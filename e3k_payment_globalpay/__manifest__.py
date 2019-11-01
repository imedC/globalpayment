# -*- coding: utf-8 -*-
{
    'name': "Global Payment Acquirer",
    'author': 'e3k',
    'category': 'Accounting',
    'summary': """Payment Acquirer: Global Payment Implementation""",
    'website': '',
    'description': """
    Global Payment Acquirer
""",
    'version': '1.0',
    'depends': ['base','payment','website_sale','website'],
    'data': [
        'views/global_payment_view.xml',
        'views/templates.xml',
        'data/payment_acquirer_data.xml',

             ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
