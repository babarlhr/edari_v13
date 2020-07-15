# -*- coding: utf-8 -*-
{
    'name': "Applicant Extension",

    'summary': """
        Erpify""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',
    

    # any module necessary for this one to work correctly
    'depends': ['base','hr_recruitment','sale','employee_custom'],

    # always loaded
    'data': [
        'views/applicant_ext_view.xml',
    ],

}
