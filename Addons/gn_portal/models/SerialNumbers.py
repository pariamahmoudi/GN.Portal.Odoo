from ..imports import fields,models,api

class SerialNumber(models.Model):
    _name = "gn.portal.serialnumbers"
    name = fields.Char()
    customer_id = fields.Many2one('res.partner', string="Customer")
    shopper_name = fields.Char(string="Shopper Name")
    purchase_date = fields.Date(string="Purchase Date")
    hid = fields.Char(string="HID")
    expire_date = fields.Date(string="Expires On")
    product_name = fields.Char(string = "Product Name")
    lock_description = fields.Char(string="Description")
    comments = fields.Text(string="Comments")
    categ_id = fields.Many2one(
        'product.category',string= 'Product Category')

    number_of_users = fields.Selection([
        ('single', 'Single'),
        ('2', '2'),
        ('3', '3'),
        ('5', '5'),
        ('10', '10'),
        ('15', '15'),
        ('25', '25'),
        ('35', '35'),
        ('50', '50'),
        ('75', '75'),
        ('90', '90'),
        ('150', '150'),
        ('Unlimited', 'Unlimited'),
    ])

    lock_type = fields.Selection([
        ('usb', 'USB'), 
        ('usb_net', 'USB Net '), 
        ('soft', 'نرم افزاری'), 
        ('misc', 'misc'),
        ])
    GN_Invoice = fields.Char()
