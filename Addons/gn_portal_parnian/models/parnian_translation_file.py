from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
import uuid
from ..parnian import ParnianTranslationProject

class ParnianTranslationFile(models.Model):
    _name = "gn.portal.parnian.translation.file"
    _description = 'Translation File'
    # _inherit = ['portal.mixin', 'mail.thread',
    #             'mail.activity.mixin', 'utm.mixin']

    name = fields.Char()
    guid = fields.Char(size=38, index=True, default='New')

    @api.model
    def create(self, vals):
        if vals.get('guid', 'New') == 'New':
            vals['guid'] = str(uuid.uuid4())
        result = super(ParnianTranslationFile, self).create(vals)
        return result