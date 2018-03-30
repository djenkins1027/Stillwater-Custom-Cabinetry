# -*- coding: utf-8 -*-

import dateutil
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Workorder(models.Model):

    _inherit = "mrp.workorder"

    hex_color = fields.Char(string="Hex Color", compute="_compute_hex_color")

    @api.depends('date_planned_finished')
    def _compute_hex_color(self):
        for record in self.filtered("date_planned_finished"):
            try:
                today = datetime.now()
                finish_date = fields.Datetime.from_string(record.date_planned_finished)
                delta = today - finish_date
                if delta.days < 0:
                    record['hex_color'] = 'FF4D4D' # red
                elif delta.days >= 0 and delta.days <= 2:
                    record['hex_color'] = 'FFFF99' # yellow
                else:
                    record['hex_color'] = '58D68D' # green
            except:
                record['hex_color'] = ""
