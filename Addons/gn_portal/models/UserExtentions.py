# -*- coding: utf-8 -*-

from odoo import models, fields, api

class UserSign(models.Model):
    _inherit = 'res.users'

    quote_signature = fields.Image(stirng='quote Signature', help='Signature received through the portal.', copy=False, attachment=True, max_width=1024, max_height=1024)

    