
from odoo import models, fields, api

from ..imports import ProductProduct, ProductTemplate

class ProductExtensions(ProductProduct):
    _inherit = "product.product"
    #gn_synch_data = fields.Char()
    
    

class ProductTemplateExtensions(ProductTemplate):
    _inherit = "product.template"
    gn_synch_data = fields.Char()


