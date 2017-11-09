# coding: utf-8

from odoo import api, fields, models, _

class PaymentAcquirerCheckout(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('checkout', 'Checkout.com')])
    checkout_secret_key = fields.Char(required_if_provider='checkout', groups='base.group_user')
    checkout_publishable_key = fields.Char(required_if_provider='checkout', groups='base.group_user')
    checkout_image_url = fields.Char(
        "Checkout Image URL", groups='base.group_user',
        help="A relative or absolute URL pointing to a square image of your "
             "brand or product. As defined in your Checkout profile. See: "
             "https://docs.checkout.com/")
