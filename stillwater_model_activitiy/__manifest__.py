# -*- coding: utf-8 -*-
{
    'name': 'Stillwater Costume Contractor Customizations',
    'version': '1.0',
    'category': 'Extra',
    'author': 'Stillwater Costume Cabinetry',
    'depends': [
        'crm', 'sale', 'quality', 'mrp'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/rooms_view.xml',
        'views/finish_code_views.xml',
        'views/quality_view.xml',
        'views/sale_view.xml',
        'views/purchase_view.xml',
        'views/workorder_views.xml',
    ],
}
