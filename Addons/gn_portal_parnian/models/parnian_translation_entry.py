from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
import uuid

if TYPE_CHECKING:
    from gn_imports import ParnianTranslationProject
else:
    ParnianTranslationProject = models.Model

class ParnianTranslationEntry(models.Model):
    _name = "gn.portal.parnian.translation.entry"
    _description = 'Translation Entry'
    # _inherit = ['portal.mixin', 'mail.thread',
    #             'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string="Name", default="New")
    # key = fields.Char(string = "Key")
    guid = fields.Char(size=38, index=True, default='New')
    ar = fields.Text(string="Ar")
    fa = fields.Text(string="Fa")
    en = fields.Text(string="En")
    key1 =fields.Char(string="Key1")
    key2 =fields.Char(string="Key2")
    key3 =fields.Char(string="Key3")
    fromVersion = fields.Char(string="From Version")
    toVersion = fields.Char(string="To Version")
    tag = fields.Char(string="Tag")
    jsonData = fields.Text(string="Data")
    project_id = fields.Many2one('gn.portal.parnian.translation.project')
    file_id = fields.Many2one('gn.portal.parnian.translation.file')
    state = fields.Selection([
        ('approved', "Approved"),
        ('inprogress', "In Progress"),
        ('cancel', "Cancel")], 
        default="inprogress", 
        string="Status")
    untranslatable = fields.Boolean(string="Untranslatable")


    @api.model
    def create(self, vals):
        if vals.get('guid', 'New') == 'New':
            vals['guid'] = str(uuid.uuid4())
        result = super(ParnianTranslationEntry, self).create(vals)
        return result

    
    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            if isinstance(name,str):
                splt = name.split('|')
                name = splt[len(splt)-1]
            result.append((rec.id, '{} : {}'.format(rec.id, name)))
        return result