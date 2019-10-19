# -*- coding: utf-8 -*-
{
    'name': 'Purchase Custom',
    'version': '13.0.01',
    'author': 'ERPfy.co',
    'website': 'www.erpfy.co',
    'summary': 'Add summary here',
    'description': """
    Add description here.
    """,
    'depends': [
        'base', 'purchase', 'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase.xml',
        'views/template.xml',
        'views/tags_views.xml',
    ],
    'installable': True,
}

