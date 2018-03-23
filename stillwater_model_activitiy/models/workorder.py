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
        for record in self:
            try:
                for record in self.filtered("date_planned_finished"):
                    delta = datetime.now() - fields.Datetime.from_string(record.date_planned_finished)
                    if delta.days > 14:
                        record['hex_color'] = '58D68D' # green
                    elif delta.days <= 14 and delta.days > 7:
                        record['hex_color'] = 'F7DC6F' # yellow
                    elif delta.days <= 7 and delta.days > 0:
                        record['hex_color'] = 'F39C12' # orange
                    elif delta.days < 0:
                        record['hex_color'] = 'E74C3C' # red
            except:
                record['hex_color'] = ""