from odoo import models, fields, api, _


class Contact(models.Model):
    _inherit = 'res.partner'

    eCode = fields.Char()
    nID = fields.Char()
