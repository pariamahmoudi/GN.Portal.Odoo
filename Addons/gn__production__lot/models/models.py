# -*- coding: utf-8 -*-

from odoo import models, fields, api


class gn__production__lot(models.Model):
    _name = 'gn__production__lot.gn__production__lot'
    _description = 'gn__production__lot.gn__production__lot'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    Customer_id = fields.Many2one('res.partner', string='Customer')

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
