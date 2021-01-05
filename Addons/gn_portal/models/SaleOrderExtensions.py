# -*- coding: utf-8 -*-

from ..imports import fields,models,SaleOrder,SaleOrderLine,api , GregorianToJalali ,main 

class SaleOrderExtensions(SaleOrder):
    _inherit = 'sale.order'
    gn_reciever = fields.Many2one('res.partner')
    gn_calculate_date = fields.Char(compute="calculate_date")
    gn_pricetoalpha = fields.Char(compute="price_calculation")
    @api.depends('gn_create_date_override')
    def _compute_overrides(self):
        for order in self:
            order.gn_override = "{}".format(order.gn_create_date_override)
            if order.gn_create_date_override:
                order.env.cr.execute("UPDATE sale_order SET create_date='%s' WHERE id=%s" %    
                    (order.gn_create_date_override,order.id))  

    @api.depends('date_order')
    def calculate_date(self):
        for order in self:
            p = GregorianToJalali(order.date_order.year , order.date_order.month , order.date_order.day)
            order.gn_calculate_date = "{}/{}/{}".format(p.jyear, p.jmonth ,p.jday  )
    @api.depends('amount_total')
    def price_calculation(self):
        for order in self:
            p = main(order.amount_total)      
            order.gn_pricetoalpha = p




    #     self.env.cr.execute("UPDATE report_rental_income_from_property SET create_date='%s', create_uid=%s, write_date='%s', write_uid=%s WHERE id=%s" % 
    # (value['create_date'], value['create_uid'], value['write_date'], value['write_uid'], property_id))
    gn_description = fields.Char(string="description")
    gn_synch_data = fields.Char(string='SynchData')
    gn_create_date_override = fields.Datetime()
    gn_override = fields.Char(compute=_compute_overrides)
    gn_quotenumber = fields.Integer(string="Quote No.")
    
    def create_invoice(self, args=False):
        print('create_invoice')
        for order in self:
            m = self.env['sale.advance.payment.inv'].create({}).with_context({'active_ids':order.id})
            #self._context['active_ids'] = order.id
            m.create_invoices()
            

        return True
    def some_action(self, args=False):
        print('some_action')
        for order in self:
            _o:SaleOrderExtensions = order
            print(_o.name)
        return True
        

    


class SaleOrderLineExtensions(SaleOrderLine):
    _inherit = 'sale.order.line'
    gn_tax_percentage = fields.Float()
    gn_synch_data = fields.Char(string='SynchData')
