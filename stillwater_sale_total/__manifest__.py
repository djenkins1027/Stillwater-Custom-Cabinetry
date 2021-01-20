# -*- coding: utf-8 -*-
{
    'name': 'Stillwater Custom Cabinetry: Modify Calculation of Subtotal Field on Sales Order',
    'summary': 'Modify Calculation of Subtotal Field on Sales Order',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '1.1',
    'author': 'Odoo Inc',
    'description': """
        Task ID: 2420314
        - Calculate Subtotal based on the product total
    """,
    'category': 'Custom Development',

    # any module necessary for this one to work correctly
    'depends': ['sale'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
