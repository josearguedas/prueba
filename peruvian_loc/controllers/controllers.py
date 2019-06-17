# -*- coding: utf-8 -*-
from odoo import http

# class PeruvianLoc(http.Controller):
#     @http.route('/peruvian_loc/peruvian_loc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/peruvian_loc/peruvian_loc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('peruvian_loc.listing', {
#             'root': '/peruvian_loc/peruvian_loc',
#             'objects': http.request.env['peruvian_loc.peruvian_loc'].search([]),
#         })

#     @http.route('/peruvian_loc/peruvian_loc/objects/<model("peruvian_loc.peruvian_loc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('peruvian_loc.object', {
#             'object': obj
#         })