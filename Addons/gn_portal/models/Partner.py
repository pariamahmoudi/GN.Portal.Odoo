# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    GN_Fax = fields.Integer()
    GN_Telegram = fields.Integer()
    GN_CommercialCode = fields.Integer()
    GN_NationalID = fields.Integer()
