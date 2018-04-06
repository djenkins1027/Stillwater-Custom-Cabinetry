# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Rooms(models.Model):
    _name = "rooms.rooms"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Rooms"

    name = fields.Char("Name")
    project_lead_id = fields.Many2one("crm.lead", string="Project")
    finish_code_id = fields.Many2one("finish.code", string="Finish Code")
    mv_work_order_no = fields.Char("MV Work Order Number")
    contact_name = fields.Char(string="Home Owner Last Name", related="project_lead_id.contact_name")
    mv_project_no = fields.Char(string="MV Project Number", related="project_lead_id.mv_project_no")
    bad_sq_ft = fields.Char("Bad Sq. Ft")
    expected_ship_date = fields.Date("Expected Ship Date", store=False,related="project_lead_id.ship_date")
    triple_binder_deadline = fields.Date("Triple Binder Deadline", conpute="_compute_triple_binder_deadline")
    final_decision_date = fields.Date("Final Decision Date", conpute="_compute_triple_binder_deadline")
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
    quality_room_count = fields.Integer("Quality Rooms count", compute="_compute_quality_room_count")
    so_romm_count = fields.Integer("Sale Rooms count", compute="_compute_so_room_count")
    sq_ft = fields.Integer("Sq. Ft.")
    quotation_ids = fields.Many2many(comodel_name='sale.order', string="Quotation")


    @api.depends('expected_ship_date')
    def _compute_triple_binder_deadline(self):
        for record in self:
            record.triple_binder_deadline = dateutil.parser.parse(record.expected_ship_date).date() - datetime.timedelta(days=35)

    @api.depends('expected_ship_date')
    def _compute_triple_binder_deadline(self):
        for record in self:
            record.triple_binder_deadline = dateutil.parser.parse(record.expected_ship_date).date() - datetime.timedelta(days=35)

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
