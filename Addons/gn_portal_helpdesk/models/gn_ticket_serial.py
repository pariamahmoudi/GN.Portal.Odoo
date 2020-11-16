from odoo import models, fields, api

class helpdeskcustomization(models.Model):
    _inherit = 'helpdesk.ticket' 

    gn_serial_number = fields.Many2one('gn.portal.serialnumbers')