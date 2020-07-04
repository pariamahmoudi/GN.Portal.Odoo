# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pyodbc


class gn__production__lot(models.Model):
    _name = 'gn__production__lot.gn__production__lot'
    _description = 'gn__production__lot.gn__production__lot'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    p = fields.Text()
    changed = fields.Text()
    Customer_id = fields.Many2one('res.partner', string='Customer')

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
    
 
    
    @api.onchange('value')
    def _compute_note(self):

        self.p = "the value is {}".format(self.value)
        
    
    
    @api.onchange('value')
    def compute_note(self):
        if self.p :
            splitted = self.p.split()
            if splitted[3] != self.value:
                self.p = "the value is {}".format(self.value)
                self.changed = "p changed to {}".format(self.value)
            else:
                pass

    @api.onchange('value')
    
    def db_connect(self):
        
        conn = pyodbc.connect("Driver={SQL Server};Server=GNTCRM365P;Database=Epidemi_MSCRM;Uid=Paria;Pwd=P@ssw0rdGN;")
        cursor = conn.cursor()
        cursor.execute("SELECT TOP (30)" 

        "[ContactId],[Salutation],[FirstName],[LastName],[FullName],[Description],[MobilePhone],[Telephone1],[gn_IDCardNumber],[gn_NationalCode]"
        ",[gn_PatientUID],[gn_Lat],[gn_Long],[gn_RelatedPOCU] " 
        "FROM [Epidemi_MSCRM].[dbo].[Contact] where FullName is not null ")
        for row in cursor:
            # print('contactid={contactid}'.format(contactid=row.ContactId))
            partner = self.env['res.partner'].create({'name' :row.FullName}) #work but don't save
            # self.env['test.store'].create({'id_store': 100}) #work but don't save
 

        
    


        
        
        
        
        