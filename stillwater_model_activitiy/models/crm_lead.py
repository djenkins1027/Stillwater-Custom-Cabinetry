# -*- coding: utf-8 -*-

from odoo import api, fields, models, _



class CrmLead(models.Model):
    _inherit = "crm.lead"
    
    mv_project_no = fields.Char(string="MV Project Number")
    ship_date = fields.Date(string="Expected Ship Date")