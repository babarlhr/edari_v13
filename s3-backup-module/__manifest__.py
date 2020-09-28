# -*- coding: utf-8 -*-
{
    'name': "Manual Database Backup to Amazon S3",

    'summary': """
        Database Backup to Amazon s3 bucket""",

    'description': """
        Backup your database using the dependent module and add backup of the database file to S3 bucket directly
    """,

    'author': "Erpify",
    'website': "",
    'sequence': '10',
    'category': 'Backup',
    'version': '13.0.1.0.0',
    'external_dependencies': {'python': ['boto']},

    # any module necessary for this one to work correctly
    'depends': ['base', 'auto_backup'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/s3_backup.xml',
    ],

    # only loaded in demonstration mode
    'demo': [

    ],

    'auto_install': False,
    'installable': True,
    # 'images': ['static/description/storage.JPG'],
}
