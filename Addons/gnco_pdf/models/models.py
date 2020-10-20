# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UserSign(models.Model):
    _inherit = 'res.users'

    signature = fields.Image('Signature', help='Signature received through the portal.', copy=False, attachment=True, max_width=1024, max_height=1024)

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    additional_note = fields.Text(default="this is added by default")
    official_pay = fields.Text(default="gostareh\n 6219861036941705")
    unofficial_pay = fields.Text(default="حسین\n  شماره کارت 5022291092771513")


    def convertnum(self):
        return "paria"
class gnco_pdf(models.Model):
    _name = 'gnco_pdf.gnco_pdf'
    _description = 'gnco_pdf.gnco_pdf'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    
    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
