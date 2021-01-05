# -*- coding: utf-8 -*-
{
    'name': "GN.Portal.Bot",

    'summary': """
        Gostareh Negar Portal Bot Extensions
    """,

    'description': """
        Extends odoo bot.
    """,

    'author': "Gosrateh Negar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail_bot'],

    # always loaded
    'data': [

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'application': False,
    'installable': True,
}
