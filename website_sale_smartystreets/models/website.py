# -*- coding: utf-8 -*-

from odoo import fields, models

class WebisteAccessKey(models.Model):
    _inherit = 'website'

    smart_auth_id    = fields.Char(String='SMART AUTH ID ')
    
    auth_token_id    = fields.Char(String='SMART AUTH TOKEN ')