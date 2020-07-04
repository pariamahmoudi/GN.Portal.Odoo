from odoo import models, fields, api, _


class technical_spec(models.Model):
    _inherit = 'product.template'

    Data_sheet = fields.Selection([ ('type1', 'Type 1'),('type2', 'Type 2'),],'Type', default='type1')
    test = fields.Char()
    
    @api.onchange('Data_sheet')
    def compute_note(self):
    
        self.description = "the value is {}".format(self.Data_sheet)