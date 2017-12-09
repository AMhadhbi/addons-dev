# -*- coding: utf-8 -*-
# © 2017 bloopark systems (<http://bloopark.de>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSale(WebsiteSale):

    @http.route()
    def payment(self, **post):
        response = super(WebsiteSale, self).payment(**post)
        if not response.qcontext:
            return response

        values = response.qcontext

        return request.render(response.template, values)
