from odoo import models, fields, api, _


class Lot(models.Model):
    _inherit = 'stock.production.lot'

    customer_id = fields.Many2one('res.partner', string='customer')
