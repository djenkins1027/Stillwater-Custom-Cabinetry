# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

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
    'depends': ['quality_mrp', 'note', 'mrp_workorder'],
    'data': [
        'views/mrp_views.xml',
        'views/mrp_workorder_views.xml',
        'views/note_views.xml'
    ],
    'license': 'OEEL-1',
}
