# -*- coding: utf-8 -*-
{
    "name": "Stillwater: Product Customizations",
    'summary': "Stillwater Product Label Report",
    'description': """
Stillwater: Product Report customization
========================================
- Remove Price on Product Label Report
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['product'],
    'data': [
        'report/product_report.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OEEL-1',
}