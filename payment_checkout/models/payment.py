# coding: utf-8

import logging
import requests
import json
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
    
    
    
    @api.multi
    def checkout_form_generate_values(self, tx_values):
        self.ensure_one()
        
        checkout_tx_values = dict(tx_values)
        
        tx_values.get('amount'),
        tx_values.get('partner_email'),
        _logger.info('checkout_form_generate_values email %s',tx_values.get('partner_email'))
        
        temp_checkout_tx_values = {
            'company': self.company_id.name,
            'amount': tx_values.get('amount'),
            'currency': tx_values.get('currency') and tx_values.get('currency').name or '',
            'currency_id': tx_values.get('currency') and tx_values.get('currency').id or '',
            'address_line1': tx_values.get('partner_address'),
            'address_city': tx_values.get('partner_city'),
            'address_country': tx_values.get('partner_country') and tx_values['partner_country'].name or '',
            'email': tx_values.get('partner_email'),
            'address_zip': tx_values.get('partner_zip'),
            'name': tx_values.get('partner_name'),
            'phone': tx_values.get('partner_phone'),

        }
        
        temp_checkout_tx_values['returndata'] = checkout_tx_values.pop('return_url', '')
        checkout_tx_values.update(temp_checkout_tx_values)
        return checkout_tx_values
    
    @api.model
    def _get_checkout_api_url(self):
        return 'sandbox.checkout.com/api2/v2'


    def _get_feature_support(self):
        """Get advanced feature support by provider.

        Each provider should add its technical in the corresponding
        key for the following features:
            * fees: support payment fees computations
            * authorize: support authorizing payment (separates
                         authorization and capture)
            * tokenize: support saving payment data in a payment.tokenize
                        object
        """
        res = super(PaymentAcquirerCheckout, self)._get_feature_support()
        res['tokenize'].append('checkout')
        return res

class PaymentTransactionCheckout(models.Model):
    _inherit = 'payment.transaction'
    
    
    def _create_checkout_charge(self, post):
        
        _logger.info("######################### _create_checkout_charge ")
        
        _logger.info("######################### _create_checkout_charge post %s",post)
        
        _logger.info("######################### post.get%s  ",post.get('email'))
        
        api_url_charge = 'https://%s/charges/token' % (self.acquirer_id._get_checkout_api_url())
        
        headers = {'content-type': 'application/json',
           'Authorization': self.acquirer_id.checkout_secret_key}
        
        _logger.info("######################### headers %s ",headers)
        
        charge_params = {
          "autoCapTime": "0",
          "autoCapture": "Y",
          "chargeMode": 1,
          "email": post.get('email'),
          "description": self.reference,
          "value": float(post.get('value')),
          "currency":post.get('currency'),
          "cardToken":  post.get('cardToken'),
          }

        response = requests.post(api_url_charge, data=json.dumps(charge_params), headers=headers)
        
        data=response.json()
        _logger.info('checkout_create_charge data.json() %s',data)
        data['metadata']['reference']=self.reference
        
        _logger.info('checkout_create_charge data 222 %s',data)
        
        
        return data


    @api.model
    def _checkout_form_get_tx_from_data(self, data):
        """ Given a data dict coming from Checkout, verify it and find the related
        transaction record. """
        
        _logger.info("#######data %s",data)
        medatada = data.get('metadata', {}).get('reference')
        
        _logger.info("######medatada %s",medatada)

        reference =data['metadata']['reference']
        
        _logger.info("######reference %s",reference)
        
                
        if not reference:
            checkout_error = data.get('error', {}).get('message', '')
            _logger.error('Checkout: invalid reply received from Checkout API, looks like '
                          'the transaction failed. (error: %s)', checkout_error  or 'n/a')
            error_msg = _("We're sorry to report that the transaction has failed.")
            if checkout_error:
                error_msg += " " + (_("Checkout gave us the following info about the problem: '%s'") %
                                    checkout_error)
            error_msg += " " + _("Perhaps the problem can be solved by double-checking your "
                                 "credit card details, or contacting your bank?")
            raise ValidationError(error_msg)

        tx = self.search([('reference', '=', reference)])
        if not tx:
            error_msg = (_('Checkout: no order found for reference %s') % reference)
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        elif len(tx) > 1:
            error_msg = (_('Checkout: %s orders found for reference %s') % (len(tx), reference))
            _logger.error(error_msg)
            raise ValidationError(error_msg)
        return tx[0]
    
    
    @api.multi
    def _checkout_form_get_invalid_parameters(self, data):
        
        _logger.info("######################### _checkout_form_get_invalid_parameters")
        
        _logger.info("######################### data %s",data)
                     
        invalid_parameters = []
        reference = data['metadata']['reference']
        if reference != self.reference:
            invalid_parameters.append(('Reference', reference, self.reference))
        return invalid_parameters
    
    
    @api.multi
    def _chechkout_form_validate(self,  data):
        
        _logger.info("######################### _chechkout_form_validate")
        _logger.info("######################### data %s" ,data)
                
        return self._checkout_s2s_validate_tree(data)

    
    
    @api.multi
    def _checkout_s2s_validate_tree(self, tree):
        self.ensure_one()
        
        _logger.info("######################### _checkout_s2s_validate_tree")
        
        if self.state not in ('draft', 'pending', 'refunding'):
            _logger.info('Checkout: trying to validate an already validated tx (ref %s)', self.reference)
            return True
        
        
        _logger.info("######################### tree %s" ,tree)
         
        status = tree.get('status')
        if status == 'succeeded':
            new_state = 'refunded' if self.state == 'refunding' else 'done'
            self.write({
                'state': new_state,
                'date_validate': fields.datetime.now(),
                'acquirer_reference': tree.get('id'),
            })
            self.execute_callback()
            if self.payment_token_id:
                self.payment_token_id.verified = True
            return True
        else:
            error = tree['error']['message']
            _logger.warn(error)
            self.sudo().write({
                'state': 'error',
                'state_message': error,
                'acquirer_reference': tree.get('id'),
                'date_validate': fields.datetime.now(),
            })
            return False
