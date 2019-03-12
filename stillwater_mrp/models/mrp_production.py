# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    sale_line_id = fields.Many2one('sale.order.line')
    spec_group = fields.Char(string="MV Spec Group Name", related="sale_line_id.spec_group")

    def _generate_raw_move(self, bom_line, line_data):
        res = super(MrpProduction, self)._generate_raw_move(bom_line, line_data)
        res.sale_line_id = self.sale_line_id.id
        return res


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, values, bom):
        vals = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, values, bom)
        if values['move_dest_ids'] and values['move_dest_ids'].sale_line_id:
            sale_line_id = values['move_dest_ids'].sale_line_id
            vals['sale_line_id'] = sale_line_id.id
        return vals


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_procurement_values(self):
        res = super(StockMove, self)._prepare_procurement_values()
        res['sale_line_id'] = self.sale_line_id.id
        return res
