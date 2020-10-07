# -*- coding: utf-8 -*-

#from odoo import models, fields, api
from ..imports import models, fields,api, AccountMove, AccountMoveLine

class AccountInvoiceExtensions(AccountMove):
    _inherit = 'account.move'

    gn_synch_data = fields.Char()
    gn_invoice_number = fields.Char(string="Invoice Number")
    gn_official_invoice_index = fields.Integer(string="Official Number")
    gn_invoice_date = fields.Date()

class AccountMoveLineExtensions(AccountMoveLine):
    _inherit = 'account.move.line'

    gn_synch_data = fields.Char()


