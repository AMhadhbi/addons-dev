# -*- coding: utf-8 -*-

import logging
import werkzeug
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)

class CheckoutController(http.Controller):


    @http.route(['/payment/checkout/create_charge'], type='json', auth='public')
    def checkout_create_charge(self, **post):
        """ Create a payment transaction

        Expects the result from the user input from checkout.js popup"""
        
        TX = request.env['payment.transaction']
        tx = None
        
        if post.get('tx_ref'):
            tx = TX.sudo().search([('reference', '=', post.get('tx_ref'))])
        if not tx:
            tx_id = (post.get('tx_id') or request.session.get('sale_transaction_id') or
                     request.session.get('website_payment_tx_id'))
            tx = TX.sudo().browse(int(tx_id))
        if not tx:
            raise werkzeug.exceptions.NotFound()
        
        response = tx._create_checkout_charge(post)
        if response:
            request.env['payment.transaction'].sudo().form_feedback(response, 'checkout')
        return post.pop('return_url', '/')
    