# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import Counter
from datetime import datetime

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round

class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"
    _description = "Record Production"

    def do_produce(self):
        ret =  super(MrpProductProduce, self).do_produce()
        if self.production_id.state in ('progress', 'done'):
            for move in self.production_id.move_raw_ids:
                # TODO currently not possible to guess if the user updated quantity by hand or automatically by the produce wizard.
                if move.product_id.tracking == 'none' and move.state not in ('done', 'cancel') and move.unit_factor and move.quantity_done < move.product_uom_qty:
                    rounding = move.product_uom.rounding
                    if self.product_id.tracking != 'none':
                        qty_to_add = float_round(move.product_uom_qty - move.quantity_done, precision_rounding=rounding)
                        move._generate_consumed_move_line(qty_to_add, self.lot_id)
                    else:
                        move.quantity_done += float_round(move.product_uom_qty - move.quantity_done, precision_rounding=rounding)
        return ret
