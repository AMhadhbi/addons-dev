# -*- coding: utf-8 -*-

from odoo import fields, models,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    smart_auth_id    = fields.Char(String='SMART AUTH ID',  related='website_id.smart_auth_id')
    
    auth_token_id    = fields.Char(String='SMART AUTH TOKEN ',  related='website_id.auth_token_id')
    
    has_smarty_streets  = fields.Boolean(String='SmartyStreets API',related='website_id.has_smarty_streets')
    
    
    @api.onchange('has_smarty_streets')
    def onchange_has_smarty_streets(self):
        if not self.has_smarty_streets:
            self.smart_auth_id = False
            self.auth_token_id = False
            
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('smart_auth_id', (self.access_key or '').strip())
        set_param('auth_token_id', (self.access_key or '').strip())
        set_param('has_smarty_streets', self.has_smarty_streets)
        