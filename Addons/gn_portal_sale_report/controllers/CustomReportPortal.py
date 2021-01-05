# -*- coding: utf-8 -*-
# from odoo import http
from odoo import fields, http, _
from odoo.addons.sale.controllers.portal import CustomerPortal

class CustomerPortal(CustomerPortal):
    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw): 
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        print("******************************************************")
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type, report_ref='gn_portal_sale_report.report_gnco_quote_temp', download=download)
        return super(CustomerPortal , self).portal_order_page(order_id, report_type, access_token, message, download)