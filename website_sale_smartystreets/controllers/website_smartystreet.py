# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route
from odoo import _
import requests

import logging
_logger = logging.getLogger(__name__)


from smartystreets import Client


class WebsiteSmartyStreet(WebsiteSale):

        
    def checkout_form_validate(self, mode, all_form_values, data):
         
        res = super(WebsiteSmartyStreet, self).checkout_form_validate(mode, all_form_values,data)
 
        smart_auth_id = request.env['ir.config_parameter'].sudo().get_param('smart_auth_id')

        auth_token = request.env['ir.config_parameter'].sudo().get_param('auth_token_id')
        
        client = Client(smart_auth_id, auth_token)

        address = client.street_address("100 Main St Richmond, VA")
        
        _logger.info("################### address%s",address)

        address.confirmed

        _logger.info("###################  address.verified%s", address.confirmed)
        
        return res
