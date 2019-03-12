# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FinishCode(models.Model):
    _name = "finish.code"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Finish Code"

    name = fields.Char('Name')
