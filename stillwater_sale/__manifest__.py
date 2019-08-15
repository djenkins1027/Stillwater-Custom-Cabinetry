# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Stillwater: Sale Customizations",
    'summary': "Web",
    'description': """
Stillwater: Sales customization
===============================
- Compute price unit based on 'Calculator' field on sale order line
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_views.xml'
    ],
    'license': 'OEEL-1',
}
