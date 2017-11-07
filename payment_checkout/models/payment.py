# coding: utf-8

import logging
import requests

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


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

