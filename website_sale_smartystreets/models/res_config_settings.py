# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    smart_auth_id    = fields.Char(String='SMART AUTH ID',  related='website_id.smart_auth_id')
    
    auth_token_id    = fields.Char(String='SMART AUTH TOKEN ',  related='website_id.auth_token_id')
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('smart_auth_id', (self.access_key or '').strip())
        set_param('auth_token_id', (self.access_key or '').strip())