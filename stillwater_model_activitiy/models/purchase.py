# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_id = fields.Many2one('sale.order', 'Sale Order')

    @api.model
    def create(self, vals):
        if vals.get('origin'):
            sale_id = self.env['sale.order'].search([('name', '=',vals.get('origin'))], limit=1)
            if sale_id:
                vals.update({'sale_id': sale_id.id})
        return super(PurchaseOrder, self).create(vals)
 
    @api.multi
    def write(self, vals):
        if vals.get('origin'):
            sale_id = self.env['sale.order'].search([('name', '=',vals.get('origin'))], limit=1)
            if sale_id:
                vals.update({'sale_id': sale_id.id})
        return super(PurchaseOrder, self).write(vals)