# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route
from odoo import _
import requests

class WebsiteNumverify(WebsiteSale):

    def _get_country(self,data):
            
            country = request.env['res.country']

            if data.get('country_id'):
            
                country = country.browse(int(data.get('country_id')))
                
                country_code =country.code
            
            return country_code
        
    def checkout_form_validate(self, mode, all_form_values, data):
        
        res = super(WebsiteNumverify, self).checkout_form_validate(mode, all_form_values,data)
        
        has_numverify = request.env['ir.config_parameter'].sudo().get_param('has_numverify')
        
        access_key = request.env['ir.config_parameter'].sudo().get_param('access_key')
        
        if access_key and has_numverify:
            
            if not data.get('phone'):
                
                res[0]["phone"] = 'missing'
                res[1].append(_('Phone fields are empty.'))
            
            if data.get('phone'):
                       
                country_code=self._get_country(data)
                
                url = 'http://apilayer.net/api/validate?access_key=' + access_key + '&number=' + data.get('phone')+'&country_code='+country_code
                
                response = requests.get(url)
                
                r=response.json()
                
                answer = r['valid']
                
                if answer == False:
                    
                    res[0]["phone"] = 'error'
                    
                    res[1].append(_('Invalid Phone! Please enter a phone Number.'))
                    
        return res
