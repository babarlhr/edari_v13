{
    'name': "Salary Sheet",
    'description': "Salary Sheet",
    'author': 'E-cube',
    'website': "ecube.pk",
    'category': 'sale',
    'version': '13.0.01',
    'application': True,
    'depends': ['base','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'template.xml',
        'views/module_report.xml',
    ],
}