from odoo import models, fields, api

class TicketWizard(models.Model):
    _name='gn_ticket_wizard'

    priority = fields.Selection([
        ('medium', "Medium"),
        ('high', "Heigh"),
        ('low', "Low"),
        ], 
        default="medium", 
        string="Priority")