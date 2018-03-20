# -*- coding: utf-8 -*-
{
    "name": "Stillwater: Mrp Customizations",
    'summary': "Web",
    'description': """
Stillwater: Mrp Customizations
==============================
- Ability to update the 'To Consume' in Consumed Matirials when MO is in confirmed state.
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['mrp', 'quality_mrp'],
    'data': [
        'views/mrp_views.xml'
    ],
    'license': 'OEEL-1',
}