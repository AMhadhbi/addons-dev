# -*- coding: utf-8 -*-
# © 2017 bloopark systems (<http://bloopark.de>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Website Sale - Info Panels",
    'summary': """
        Add info panels to the delivery and payment
        services of your online shop.""",
    'description': """
    """,
    'version': '10.0.1.0.0',
    'author': 'bloopark systems GmbH & Co. KG',
    'website': 'http://www.bloopark.de',
    'license': 'AGPL-3',
    'category': 'e-commerce',
    'depends': [
        'website_sale_delivery'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/website_sale_info.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}