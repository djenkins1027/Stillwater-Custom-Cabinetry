# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        group_id = vals.get('group_id', False)
        group = self.env['procurement.group'].browse(group_id)
        vals.update({'x_studio_field_ZFXHm': group.sale_id.id})
        return super(PurchaseOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        vals.update({'x_studio_field_ZFXHm': self.group_id.sale_id.id})
        return super(PurchaseOrder, self).write(vals)
