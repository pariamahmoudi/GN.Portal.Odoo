from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
import uuid

if TYPE_CHECKING:
    from gn_imports import ParnianTranslationProject
else:
    ParnianTranslationProject = models.Model

class ParnianTranslationBranch(models.Model):
    _name = "gn.portal.parnian.translation.branch"
    _description = 'Translation Branch'
    # _inherit = ['portal.mixin', 'mail.thread',
    #             'mail.activity.mixin', 'utm.mixin']

    name = fields.Char()
    @api.model
    def create(self, vals):
        if vals.get('guid', 'New') == 'New':
            vals['guid'] = str(uuid.uuid4())
        result = super(ParnianTranslationBranch, self).create(vals)
        return result
