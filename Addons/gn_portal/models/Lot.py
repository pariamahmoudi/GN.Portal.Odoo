# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Lot(models.Model):
    _inherit = 'stock.production.lot'

    GN_CustomerId = fields.Many2one('res.partner')
    GN_PurchaseDate = fields.Date()
    GN_HID = fields.Integer()
    GN_ExpireDate = fields.Date()
    GN_Dongletype = fields.Selection([('value1', 'Single'), ('value2', 'Multi 3'), ('value3', 'Multi 5'), ('value4', 'Multi 10'), ('value5', 'Multi 15'), ('value6', 'Multi 25'), ('value7', 'Unlimited')])
    GN_Invoice = fields.Char()
    

    