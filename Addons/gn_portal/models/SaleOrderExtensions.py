# -*- coding: utf-8 -*-

from ..imports import fields,models,SaleOrder,SaleOrderLine,api , GregorianToJalali

class SaleOrderExtensions(SaleOrder):
    _inherit = 'sale.order'
    gn_additional_note = fields.Text(default="تاریخ یک هفته\n هزینه ارسال با مشتری")
    gn_reciever = fields.Many2one('res.partner')
    gn_calculate_date = fields.Char(compute="calculate_date")
    gn_official_pay = fields.Text(default="شماره حساب 1-2679689-810-832 \n شماره کارت 848646 \n ir5454 شماره شبا   \n گستره نگار حامی پرنیان \n بانک سامان")
    gn_unofficial_pay = fields.Text(default="شماره حساب 1-2679689-810-832 \n شماره کارت 62198610 \n irشماره شبا  5454 \n حسین \n بانک سامان")
    
    @api.depends('gn_create_date_override')
    def _compute_overrides(self):
        for order in self:
            order.gn_override = "{}".format(order.gn_create_date_override)
            if order.gn_create_date_override:
                order.env.cr.execute("UPDATE sale_order SET create_date='%s' WHERE id=%s" %    
                    (order.gn_create_date_override,order.id))  

    @api.depends('date_order')
    def calculate_date(self):
        
        p = GregorianToJalali(self.date_order.year , self.date_order.month , self.date_order.day)
        self.gn_calculate_date = "{}/{}/{}".format(p.jyear, p.jmonth ,p.jday  )
        




    #     self.env.cr.execute("UPDATE report_rental_income_from_property SET create_date='%s', create_uid=%s, write_date='%s', write_uid=%s WHERE id=%s" % 
    # (value['create_date'], value['create_uid'], value['write_date'], value['write_uid'], property_id))
    GN_Organization = fields.Selection([('gn', 'Gostareh'), ('hami', 'Hami')])
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
