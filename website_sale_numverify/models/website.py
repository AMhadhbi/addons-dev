# -*- coding: utf-8 -*-

from odoo import fields, models

class WebisteAccessKey(models.Model):
    _inherit = 'website'

    access_key  = fields.Char(String='Access key ')
