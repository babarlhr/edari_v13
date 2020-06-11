# -*- coding: utf-8 -*-
{
    'name': "Applicant Extension",

    'summary': """
        Erpify""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',

    # any modules necessary for this one to work correctly
    'depends': ['base','hr_recruitment','sale'],

    # always loaded
    'data': [
        'views/applicant_ext_view.xml',
    ],

}
