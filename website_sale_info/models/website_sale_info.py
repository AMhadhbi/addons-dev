# -*- coding: utf-8 -*-
# © 2017 bloopark systems (<http://bloopark.de>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class WebsiteSaleInfo(models.Model):
    _name = 'website.sale.info'
    _rec_name = 'title'

    type = fields.Selection(required=True, default='delivery', selection=[
        ('delivery', 'Delivery'),
        ('payment', 'Payment'),
    ], help='Show the info in the checkout page based on the type.'
            '\n- "Delivery" means the info is shown after the specific '
            'delivery method\n- "Payment" means the info is shown after '
            'the specific payment method')
    title = fields.Char(size=128)
    info = fields.Html('Info Text', help='Information text to display to the '
                                         'frontend customer.')
    website_id = fields.Many2one('website', string='Website')
    delivery_id = fields.Many2one('delivery.carrier', string='Delivery Method',
                                  domain=[('website_published', '=', True)])
    payment_id = fields.Many2one('payment.acquirer', string='Payment Method',
                                 domain=[('website_published', '=', True)])

class Website(models.Model):
    _inherit = 'website'
    
    info_line=fields.One2many("website.sale.info",'website_id',string="Sale Info")
