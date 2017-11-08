# -*- coding: utf-8 -*-

from odoo import fields, models,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    access_key  = fields.Char(String='Access key ',related='website_id.access_key')
    has_numverify = fields.Boolean("Numverify API",related='website_id.has_numverify')
    
    @api.onchange('has_numverify')
    def onchange_has_numverify(self):
        if not self.has_numverify:
            self.access_key = False



    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('access_key', (self.access_key or '').strip())
        set_param('has_numverify', self.has_numverify)