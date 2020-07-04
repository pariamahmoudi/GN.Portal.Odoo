# -*- coding: utf-8 -*-
# from odoo import http


# class Gn.portal(http.Controller):
#     @http.route('/gn.portal/gn.portal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gn.portal/gn.portal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gn.portal.listing', {
#             'root': '/gn.portal/gn.portal',
#             'objects': http.request.env['gn.portal.gn.portal'].search([]),
#         })

#     @http.route('/gn.portal/gn.portal/objects/<model("gn.portal.gn.portal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gn.portal.object', {
#             'object': obj
#         })
