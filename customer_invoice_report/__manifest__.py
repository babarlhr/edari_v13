# -*- coding: utf-8 -*-
{
    # Application Information
    'name' : 'Customer Invoice Report',
    'version' : '13.0.1',
    # 'category' : 'Sales',
    'description' : """ 
        Channel Engine Odoo Connector
    """,
    'summary' : """
        Channel Engine Odoo Connector
    """,
    
    # Author Information
    'author' : 'Edari Inc.',
    'maintainer': 'ERPify',  
    'website': 'erpify.biz',
    
    # Technical Information
    'depends': ['base','sale'],
    'data': [
            'views/template.xml',
            'views/internal_layout.xml',
            'views/module_report.xml'
            ],
    
    # App Technical Information
    'installable': True,
    'auto_install': False,
    'application' : True,
    'active': True,
}