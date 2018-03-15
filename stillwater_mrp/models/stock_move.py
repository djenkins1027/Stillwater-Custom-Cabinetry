# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange('product_uom_qty')
    def onchange_quantity(self):
        if self.env.context.get('oc_flag'):
            for line in self:
                line.quantity_done = line.product_uom_qty
                print('~~~~~~~~~~~~ {}'.format(line.quantity_done))