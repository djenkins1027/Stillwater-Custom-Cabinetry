# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    document_ids = fields.One2many('note.note', 'workorder_id', string="Documents")
    document_count = fields.Integer(compute="_compute_document_count")

    def _compute_document_count(self):
        for order in self:
            order.document_count = len(order.document_ids)

    def action_open_documents(self):
        self.ensure_one()
        action_data = self.env.ref('note.action_note_note').read()[0]
        action_data['domain'] = [('workorder_id', '=', self.id)]
        action_data['context'] = {'default_workorder_id': self.id}
        return action_data

    def _generate_lot_ids(self):
        """ Generate stock move lines """
        self.ensure_one()
        MoveLine = self.env['stock.move.line']
        tracked_moves = self.move_raw_ids.filtered(
            lambda move: move.state not in ('done', 'cancel') and move.product_id.tracking != 'none' and move.product_id != self.production_id.product_id and move.bom_line_id)
        for move in tracked_moves:
            # we need quanitites based on raw_move_lines
            # qty = move.unit_factor * self.qty_producing
            qty = move.product_uom_qty
            if move.product_id.tracking == 'serial':
                while float_compare(qty, 0.0, precision_rounding=move.product_uom.rounding) > 0:
                    MoveLine.create({
                        'move_id': move.id,
                        'product_uom_qty': 0,
                        'product_uom_id': move.product_uom.id,
                        'qty_done': qty,
                        'production_id': self.production_id.id,
                        'workorder_id': self.id,
                        'product_id': move.product_id.id,
                        'done_wo': False,
                        'location_id': move.location_id.id,
                        'location_dest_id': move.location_dest_id.id,
                    })
                    qty -= 1
            else:
                MoveLine.create({
                    'move_id': move.id,
                    'product_uom_qty': 0,
                    'product_uom_id': move.product_uom.id,
                    'qty_done': qty,
                    'product_id': move.product_id.id,
                    'production_id': self.production_id.id,
                    'workorder_id': self.id,
                    'done_wo': False,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    })

    @api.depends('current_quality_check_id', 'qty_producing')
    def _compute_component_id(self):
        for wo in self.filtered(lambda w: w.state not in ('done', 'cancel')):
            if wo.current_quality_check_id.point_id:
                wo.component_id = wo.current_quality_check_id.point_id.component_id
                wo.test_type = wo.current_quality_check_id.point_id.test_type
            elif wo.current_quality_check_id.component_id:
                wo.component_id = wo.current_quality_check_id.component_id
                wo.test_type = 'register_consumed_materials'
            else:
                wo.test_type = ''
            if wo.test_type == 'register_consumed_materials' and wo.quality_state == 'none':
                moves = wo.move_raw_ids.filtered(lambda m: m.state not in ('done', 'cancel') and m.product_id == wo.component_id)
                move = moves[0]
                lines = wo.active_move_line_ids.filtered(lambda l: l.move_id in moves)
                completed_lines = lines.filtered(lambda l: l.lot_id) if wo.component_tracking != 'none' else lines
                # we need quanitites based on raw_move_lines
                # wo.component_remaining_qty = float_round(sum(moves.mapped('unit_factor')) * wo.qty_producing - sum(completed_lines.mapped('qty_done')), precision_rounding=move.product_uom.rounding)
                wo.component_remaining_qty = float_round(sum(lines.mapped('qty_done')) - sum(completed_lines.mapped('qty_done')), precision_rounding=move.product_uom.rounding)

    def record_production(self):
        self.ensure_one()
        if self.qty_producing <= 0:
            raise UserError(_('Please set the quantity you are currently producing. It should be different from zero.'))

        if (self.production_id.product_id.tracking != 'none') and not self.final_lot_id and self.move_raw_ids:
            raise UserError(_('You should provide a lot/serial number for the final product'))

        # Update quantities done on each raw material line
        # For each untracked component without any 'temporary' move lines,
        # (the new workorder tablet view allows registering consumed quantities for untracked components)
        # we assume that only the theoretical quantity was used
        for move in self.move_raw_ids:
            if move.has_tracking == 'none' and (move.state not in ('done', 'cancel')) and move.bom_line_id\
                        and move.unit_factor and not move.move_line_ids.filtered(lambda ml: not ml.done_wo):
                rounding = move.product_uom.rounding
                if self.product_id.tracking != 'none':
                    qty_to_add = float_round(move.product_uom_qty, precision_rounding=rounding)
                    move._generate_consumed_move_line(qty_to_add, self.final_lot_id)
                else:
                    move.quantity_done += float_round(move.product_uom_qty, precision_rounding=rounding)

        # Transfer quantities from temporary to final move lots or make them final
        for move_line in self.active_move_line_ids:
            # Check if move_line already exists
            if move_line.qty_done <= 0:  # rounding...
                move_line.sudo().unlink()
                continue
            if move_line.product_id.tracking != 'none' and not move_line.lot_id:
                raise UserError(_('You should provide a lot/serial number for a component'))
            # Search other move_line where it could be added:
            lots = self.move_line_ids.filtered(lambda x: (x.lot_id.id == move_line.lot_id.id) and (not x.lot_produced_id) and (not x.done_move) and (x.product_id == move_line.product_id))
            if lots:
                lots[0].qty_done += move_line.qty_done
                lots[0].lot_produced_id = self.final_lot_id.id
                move_line.sudo().unlink()
            else:
                move_line.lot_produced_id = self.final_lot_id.id
                move_line.done_wo = True

        # One a piece is produced, you can launch the next work order
        if self.next_work_order_id.state == 'pending':
            self.next_work_order_id.state = 'ready'

        self.move_line_ids.filtered(
            lambda move_line: not move_line.done_move and not move_line.lot_produced_id and move_line.qty_done > 0
        ).write({
            'lot_produced_id': self.final_lot_id.id,
            'lot_produced_qty': self.qty_producing
        })

        # If last work order, then post lots used
        # TODO: should be same as checking if for every workorder something has been done?
        if not self.next_work_order_id:
            production_moves = self.production_id.move_finished_ids.filtered(lambda x: (x.state not in ('done', 'cancel')))
            for production_move in production_moves:
                if production_move.product_id.id == self.production_id.product_id.id and production_move.has_tracking != 'none':
                    move_line = production_move.move_line_ids.filtered(lambda x: x.lot_id.id == self.final_lot_id.id)
                    if move_line:
                        move_line.product_uom_qty += self.qty_producing
                    else:
                        move_line.create({'move_id': production_move.id,
                                 'product_id': production_move.product_id.id,
                                 'lot_id': self.final_lot_id.id,
                                 'product_uom_qty': self.qty_producing,
                                 'product_uom_id': production_move.product_uom.id,
                                 'qty_done': self.qty_producing,
                                 'workorder_id': self.id,
                                 'location_id': production_move.location_id.id, 
                                 'location_dest_id': production_move.location_dest_id.id,
                        })
                elif production_move.unit_factor:
                    rounding = production_move.product_uom.rounding
                    production_move.quantity_done += float_round(self.qty_producing * production_move.unit_factor, precision_rounding=rounding)
                else:
                    production_move.quantity_done += self.qty_producing

        if not self.next_work_order_id:
            for by_product_move in self.production_id.move_finished_ids.filtered(lambda x: (x.product_id.id != self.production_id.product_id.id) and (x.state not in ('done', 'cancel'))):
                if by_product_move.has_tracking == 'none':
                    by_product_move.quantity_done += self.qty_producing * by_product_move.unit_factor

        # Update workorder quantity produced
        self.qty_produced += self.qty_producing

        if self.final_lot_id:
            self.final_lot_id.use_next_on_work_order_id = self.next_work_order_id
            self.final_lot_id = False

        # Set a qty producing
        rounding = self.production_id.product_uom_id.rounding
        if float_compare(self.qty_produced, self.production_id.product_qty, precision_rounding=rounding) >= 0:
            self.qty_producing = 0
        elif self.production_id.product_id.tracking == 'serial':
            self._assign_default_final_lot_id()
            self.qty_producing = 1.0
            self._generate_lot_ids()
        else:
            self.qty_producing = float_round(self.production_id.product_qty - self.qty_produced, precision_rounding=rounding)
            self._generate_lot_ids()

        if self.next_work_order_id and self.production_id.product_id.tracking != 'none':
            self.next_work_order_id._assign_default_final_lot_id()

        if float_compare(self.qty_produced, self.production_id.product_qty, precision_rounding=rounding) >= 0:
            self.button_finish()
        return True
