# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Proforma(models.Model):
    _inherit = 'sale.order'


    GN_Organization = fields.Selection([('value1', 'GNC'), ('value2', 'GNH')])