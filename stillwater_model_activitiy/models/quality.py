# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class QualityAlert(models.Model):

    _inherit = "quality.alert"

    rooms_id = fields.Many2one("rooms.rooms", string="Rooms")
