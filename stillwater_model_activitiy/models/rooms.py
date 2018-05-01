# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
import dateutil

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Rooms(models.Model):
    _name = "rooms.rooms"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Rooms"

    name = fields.Char("Name")
    active = fields.Boolean(string='Active', defaut=True)
    project_lead_id = fields.Many2one("crm.lead", string="Project")
    finish_code_id = fields.Many2one("finish.code", string="Finish Code")
    mv_work_order_no = fields.Char("MV Work Order Number")
    contact_name = fields.Char(string="Home Owner Last Name", related="project_lead_id.contact_name")
    mv_project_no = fields.Char(string="MV Project Number", related="project_lead_id.mv_project_no")
    bad_sq_ft = fields.Char("Bad Sq. Ft")
    today_date = fields.Date(string='Today', compute='_compute_today_date')
    expected_ship_date = fields.Date("Expected Ship Date")  
    triple_binder_deadline = fields.Date(string="Triple Binder Deadline", store=True, compute="_compute_dates")
    final_decision_date = fields.Date(string="Final Decision Deadline", store=True, compute="_compute_dates")
    days_till_final_decision = fields.Integer(string='Days Till Final Decision Deadline ', compute='_compute_dates')
    days_till_triple_binder = fields.Integer(string='Days Till Triple Binder Deadline    ', compute='_compute_dates')
    species = fields.Char("Species")
    construction_method = fields.Selection(selection=[
                                                ('3/4 Overlay', '3/4 Overlay'),
                                                ('5/4 Overlay', '5/4 Overlay'),
                                                ('3/4 Inset', '3/4 Inset'),
                                                ('5/4 Inset', '5/4 Inset'),
                                                ('3/4 Beaded Inset', '3/4 Beaded Inset'),
                                                ('5/4 Beaded Inset', '5/4 Beaded Inset')
                                            ], string="Construction Method")
    hardware_type = fields.Char("Hardware Type")
    door_stile_rail = fields.Char("Door Stile & Rail")
    center_panel = fields.Char("Center Panel")
    outside_edge = fields.Char("Outside Edge")
    drawer_style = fields.Char("Drawer Style")
    final_decisions_made = fields.Boolean("Final Decisions are Made")
    room_budget_approved = fields.Boolean("Room Budget Approved")
    sent_to_production = fields.Boolean("Sent to Production")
    quality_room_count = fields.Integer("Quality Rooms count", compute="_compute_quality_room_count")
    so_romm_count = fields.Integer("Sale Rooms count", compute="_compute_so_room_count")
    sq_ft = fields.Integer("Sq. Ft.")
    quotation_ids = fields.Many2many(comodel_name='sale.order', string="Quotation")
    hex_color = fields.Char(string="Hex Color", compute="_compute_hex_color")
    triple_binder_days = fields.Integer(string="Tripe binder Days")
    final_decision_days = fields.Integer(string="Final Decision Days")


    @api.onchange('project_lead_id')
    def onchange_expected_date(self):
        for record in self:
            if record.project_lead_id and not record.expected_ship_date:
                record.expected_ship_date = record.project_lead_id.ship_date

    @api.depends('expected_ship_date', 'triple_binder_days', 'final_decision_days')
    def _compute_dates(self):
        for record in self:
             if record.expected_ship_date:
                ship_date = fields.Date.from_string(record.expected_ship_date)
                decision_days = record.final_decision_days if record.final_decision_days else 0
                binder_days = record.triple_binder_days if record.triple_binder_days else 0

                final_decision_date = ship_date - timedelta(days=decision_days)
                triple_binder_deadline = ship_date - timedelta(days=binder_days)

                record.final_decision_date = final_decision_date
                record.triple_binder_deadline = triple_binder_deadline

                if record.final_decisions_made and record.room_budget_approved and record.final_decision_days:
                    record.days_till_triple_binder = 1
                else:
                    record.days_till_triple_binder = (triple_binder_deadline - fields.Date.from_string(fields.Date.today())).days
                record.days_till_final_decision = (final_decision_date - fields.Date.from_string(fields.Date.today())).days

    @api.depends('expected_ship_date', 'triple_binder_deadline', 'final_decision_date', 'final_decisions_made', 'room_budget_approved')
    def _compute_hex_color(self):
        for record in self:
            if not record.sent_to_production:
                try:
                    today = fields.Datetime.from_string(fields.Datetime.now())
                    binder_date = fields.Datetime.from_string(record.triple_binder_deadline)
                    final_date = fields.Datetime.from_string(record.final_decision_date)

                    if record.final_decisions_made and record.room_budget_approved and record.expected_ship_date:
                        blinder = binder_date - today

                        if today <= binder_date:
                            if blinder.days > 7:
                                record['hex_color'] = 'B3FFFF' # light blue
                            elif blinder.days <= 7 and blinder.days > 0:
                                record['hex_color'] = '3498DB' # dark blue
                        else:
                            record['hex_color'] = 'AF7AC5' # light purple

                    elif not record.expected_ship_date:
                        if record.final_decisions_made and record.room_budget_approved:
                            record['hex_color'] = '3498DB' # blue
                        else:
                            record['hex_color'] = 'FF4D4D' # red

                    else:
                        delta = final_date - today

                        if today <= final_date:
                            if delta.days > 14:
                                record['hex_color'] = '58D68D' # green
                            elif delta.days <= 14 and delta.days > 7:
                                record['hex_color'] = 'FFFF99' # yellow
                            elif delta.days <= 7:
                                record['hex_color'] = 'FFAA80' # orange
                        else:
                            record['hex_color'] = 'FF4D4D' # red
                except:
                    record['hex_color'] = ""
            else:
                record['hex_color'] = "BFBFBF" # LIGHTGRAY

    def _compute_today_date(self):
        for record in self:
            record.today_date = fields.Date.today()

    def _compute_quality_room_count(self):
        results = self.env['quality.alert'].read_group([('rooms_id', 'in', self.ids)], 'rooms_id', 'rooms_id')
        dic = {}
        for x in results: 
            dic[x['rooms_id'][0]] = x['rooms_id_count']
        for record in self: 
            record.quality_room_count = dic.get(record.id, 0)

    def _compute_so_room_count(self):
        results = self.env['sale.order'].read_group([('rooms_id', 'in', self.ids)], 'rooms_id', 'rooms_id')
        dic = {}
        for x in results:
            dic[x['rooms_id'][0]] = x['rooms_id_count']
        for record in self:
            record.so_romm_count = dic.get(record.id, 0)
