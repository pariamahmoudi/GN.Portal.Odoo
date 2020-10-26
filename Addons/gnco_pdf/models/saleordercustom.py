# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderExtensions(models.Model):
    _inherit = 'sale.order'
    gn_additional_note = fields.Text(default="اعتبار این پیش‌فاکتور به مدت یک هفته می‌باشد\n در صورت حضور کارشناس در محل مشتری هزینه ایاب و ذهاب به عهده مشتری است \n در صورت ارائه خدمات به میزان کمتر از دو ساعت صورت حساب با حداقل دو ساعت صادر می‌گردد\n برای خریدهای کمتر از ده میلیون ریال هزینه ارسال به عهده مشتری است")
