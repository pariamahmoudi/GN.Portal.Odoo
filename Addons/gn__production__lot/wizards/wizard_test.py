from odoo import models, fields, api , _
import pyodbc

class gn__production__lot_wizard(models.TransientModel):
    __name = 'gn__production__lot_wizard'

    Paria = fields.Text(default="Driver={SQL Server};Server=GNTCRM365P;Database=Epidemi_MSCRM;Uid=Paria;Pwd=P@ssw0rdGN;")
    
    
     
    def db_connect(self):
       
        conn = pyodbc.connect(self.Paria)
        cursor = conn.cursor()
        cursor.execute("SELECT TOP (30)" 

        "[ContactId],[Salutation],[FirstName],[LastName],[FullName],[Description],[MobilePhone],[Telephone1],[gn_IDCardNumber],[gn_NationalCode]"
        ",[gn_PatientUID],[gn_Lat],[gn_Long],[gn_RelatedPOCU] " 
        "FROM [Epidemi_MSCRM].[dbo].[Contact] where FullName is not null ")
        for row in cursor:
            # print('contactid={contactid}'.format(contactid=row.ContactId))
            partner = self.env['res.partner'].create({'name' :row.FullName}) #work but don't save
            # self.env['test.store'].create({'id_store': 100}) #work but don't save