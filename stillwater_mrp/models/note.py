# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class NoteNote(models.Model):
    _inherit = "note.note"

    workorder_id = fields.Many2one('mrp.workorder', 'Workorder')
