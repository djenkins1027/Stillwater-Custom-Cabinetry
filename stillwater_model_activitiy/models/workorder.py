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
                if today < finish_date:
                    delta = finish_date - today
                    print ("delta...", delta)
                    if delta.days > 14:
                        record['hex_color'] = '58D68D' # green
                    elif delta.days <= 14 and delta.days > 7:
                        record['hex_color'] = 'FFFF99' # yellow
                    elif delta.days <= 7 and delta.days > 0:
                        record['hex_color'] = 'FFAA80' # orange
                else:
                    record['hex_color'] = 'FF4D4D' # red
            except:
                record['hex_color'] = ""
