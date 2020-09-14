# -*- coding: utf-8 -*-

from ..imports import fields,models,SaleOrder,SaleOrderLine,api

class SaleOrderExtensions(SaleOrder):
    _inherit = 'sale.order'
    @api.depends('gn_create_date_override')
    def _compute_overrides(self):
        for order in self:
            order.gn_override = "{}".format(order.gn_create_date_override)
            if order.gn_create_date_override:
                order.env.cr.execute("UPDATE sale_order SET create_date='%s' WHERE id=%s" %    
                    (order.gn_create_date_override,order.id))  




    #     self.env.cr.execute("UPDATE report_rental_income_from_property SET create_date='%s', create_uid=%s, write_date='%s', write_uid=%s WHERE id=%s" % 
    # (value['create_date'], value['create_uid'], value['write_date'], value['write_uid'], property_id))
    GN_Organization = fields.Selection([('gn', 'Gostareh'), ('hami', 'Hami')])
    gn_synch_data = fields.Char(string='SynchData')
    gn_create_date_override = fields.Datetime()
    gn_override = fields.Char(compute=_compute_overrides)
    gn_quotenumber = fields.Integer(string="Quote No.")


class SaleOrderLineExtensions(SaleOrderLine):
    _inherit = 'sale.order.line'
    gn_tax_percentage = fields.Float()
    gn_synch_data = fields.Char(string='SynchData')
