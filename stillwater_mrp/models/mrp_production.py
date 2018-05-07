# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    spec_group = fields.Char(string="MV Spec Group Name")

    @api.model
    def create(self, values):
        production = super(MrpProduction, self).create(values)
        sale = production.procurement_group_id.sale_id if production.procurement_group_id.sale_id else ""
        if sale:
            line = sale.order_line.filtered(lambda l: l.product_id == production.product_id)
            production['spec_group'] = line.spec_group

        return production
