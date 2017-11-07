# -*- coding: utf-8 -*-
# © 2017 Mhadhbi Achraf systems (<https://github.com/AMhadhbi>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Checkout Payment Acquirer',
    'category': 'e-commerce',
    'summary': 'Payment Acquirer: Checkout.com Implementation',
    'version': '11.0.1.0.0',
    'description': """Checkout Payment Acquirer""",
    'author': 'Mhadhbi Achraf',
    'website': 'https://github.com/AMhadhbi',
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_checkout_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
}
