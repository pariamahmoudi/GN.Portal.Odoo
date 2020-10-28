# -*- coding: utf-8 -*-
from odoo import http


class GncoPdf(http.Controller):
    @http.route('/gnco_pdf/gnco_pdf/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/gnco_pdf/gnco_pdf/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('gnco_pdf.listing', {
            'root': '/gnco_pdf/gnco_pdf',
            'objects': http.request.env['gnco_pdf.gnco_pdf'].search([]),
        })

    @http.route('/gnco_pdf/gnco_pdf/objects/<model("gnco_pdf.gnco_pdf"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('gnco_pdf.object', {
            'object': obj
        })
