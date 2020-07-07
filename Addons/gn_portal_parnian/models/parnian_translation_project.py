
from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
import uuid

if TYPE_CHECKING:
    from gn_imports import SaleOrderLine
else:
    SaleOrder = models.Model


class ParnianTranslationProject(models.Model):
    _name = "gn.portal.parnian.translation.project"
    _description = 'Translation Project'
    # _inherit = ['portal.mixin', 'mail.thread',
    #             'mail.activity.mixin', 'utm.mixin']

    name = fields.Char()
    guid = fields.Char(size=38, index=True, default='New')

    @api.model
    def create(self, vals):
        if vals.get('guid', 'New') == 'New':
            vals['guid'] = str(uuid.uuid4())
        result = super(ParnianTranslationProject, self).create(vals)
        return result