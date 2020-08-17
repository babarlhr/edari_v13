# -*- coding: utf-8 -*-
{
    'name': "Customer Invoice Report Ext",

    'summary': """
       Odoo Customer Invoice Report Ext""",
    'author': "Rana Rizwan",
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'views/view.xml',
    ],

}
