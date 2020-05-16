# -*- coding: utf-8 -*-
from odoo import http


class GnProductionLot(http.Controller):
    @http.route('/gn__production__lot/gn__production__lot/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/gn__production__lot/gn__production__lot/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('gn__production__lot.listing', {
            'root': '/gn__production__lot/gn__production__lot',
            'objects': http.request.env['gn__production__lot.gn__production__lot'].search([]),
        })

    @http.route('/gn__production__lot/gn__production__lot/objects/<model("gn__production__lot.gn__production__lot"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('gn__production__lot.object', {
            'object': obj
        })
