# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_factor = fields.Monetary(currency_field='currency_id', string="Calculator")

    @api.onchange('price_factor')
    def onchange_price_factor(self):
        self.product_id_change()

    @api.multi
    def _get_display_price(self, product):
        # TO DO: move me in master/saas-16 on sale.order
        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            price = product.with_context(pricelist=self.order_id.pricelist_id.id).price
            if self.price_factor > 0.00:
                price = self.price_factor / self.product_uom_qty
            return price
        final_price, rule_id = self.order_id.pricelist_id.get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        context_partner = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order)
        base_price, currency_id = self.with_context(context_partner)._get_real_price_currency(self.product_id, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)
        if self.price_factor > 0.00:
            base_price = self.price_factor / self.product_uom_qty
        if currency_id != self.order_id.pricelist_id.currency_id.id:
            base_price = self.env['res.currency'].browse(currency_id).with_context(context_partner).compute(base_price, self.order_id.pricelist_id.currency_id)
        # negative discounts (= surcharge) are included in the display price
        return base_price if self.price_factor > 0.00 else max(base_price, final_price)
