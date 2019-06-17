# -*- coding: utf-8 -*-
{
    'name': "Odoo Perú Localizaciones DK",

    'summary': """
        Odoo Perú Localizaciones DK""",

    'description': """
        Odoo Perú Localizaciones DK
    """,

    'author': "Neora",
    'website': "http://www.neora.com.pe",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',        
        'views/loc_reports.xml',
        'views/registro_compras_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}