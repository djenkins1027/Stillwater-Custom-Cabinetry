# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    spec_group = fields.Char(string="MV Spec Group Name")


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, values, bom):
        vals = super(ProcurementRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, values, bom)

        if values['move_dest_ids'] and values['move_dest_ids'].sale_line_id:
            spec_group = values['move_dest_ids'].sale_line_id.spec_group
        vals['spec_group'] = spec_group if spec_group else ""

        return vals
