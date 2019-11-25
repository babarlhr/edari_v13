# -*- coding: utf-8 -*-
{
    "name": "Customer and Supplier",
    "version": "13.0.01",
    "author": "Odoo Advantage Ireland",
    "website": "www.odoo.ie",
    "category": "contacts",
    "depends": [
        'contacts', 'base', 'website_forum', 'account'
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/vendor_as_individual.xml',
        'views/contacts_menu.xml',
        'views/vendor_as_company.xml',
        'views/res_user.xml',
    ],
    'demo': [
    ],
    'installable': True,
}
