# -*- coding: utf-8 -*-
{
    # Application Information
    'name' : 'EDARI Payslip Report',
    'version' : '13.0.1',
    # 'category' : 'Sales',
    'description' : """ 
        EDARI Payslip Report
    """,
    'summary' : """
        EDARI Payslip Report
    """,
    
    # Author Information
    'author' : 'Odoo.',
    'maintainer': 'Ecube',  
    'website': 'ecube.pk',
    
    # Technical Information
    'depends': ['base','hr_payroll'],
    'data': [
            'views/template.xml',
            'views/module_report.xml'
            ],
    
    # App Technical Information
    'installable': True,
    'auto_install': False,
    'application' : True,
    'active': True,
}