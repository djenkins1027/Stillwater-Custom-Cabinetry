# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FinishCode(models.Model):
    _name = "finish.code"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Finish Code"

    name = fields.Char('Name')
