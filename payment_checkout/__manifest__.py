# -*- coding: utf-8 -*-

{
    'name': 'Checkout.com Payment Acquirer',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: Checkout.com Implementation',
    'version': '1.0',
    'author': 'Mhadhbi Achraf',
    'website': 'https://github.com/AMhadhbi',
    'description': """Checkout.com Payment Acquirer""",
    'depends': ['payment','website_sale'],
    'data': [
        'views/payment_views.xml',
        'views/payment_checkout_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
}
