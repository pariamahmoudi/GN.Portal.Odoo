# -*- coding: utf-8 -*-

from odoo import models, fields, api

from ..imports import Partner

class PartnerExtensions(Partner):
    _inherit = 'res.partner'
    gn_fax = fields.Char()
    gn_Teleram = fields.Char()
    gn_economic_code = fields.Char()
    gn_national_code = fields.Char()
    gn_registration_code = fields.Char()
    gn_first_name = fields.Char(string="First Name")
    gn_last_name = fields.Char(string="Last Name")
    gn_synch_data = fields.Char()
    gn_salutation = fields.Char()
    

    @api.onchange('gn_last_name', 'gn_first_name')
    def _onchange_first_last_name(self):
        for i in self:
            if i.gn_first_name and i.gn_last_name:
                i.name = (i.gn_first_name + ' ' + i.gn_last_name)




    
        
