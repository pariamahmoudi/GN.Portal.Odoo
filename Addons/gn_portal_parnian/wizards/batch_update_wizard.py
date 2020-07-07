from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
if TYPE_CHECKING:
    from gn_imports import ParnianTranslationProject
else:
    ParnianTranslationProject = models.Model

class BatchUpdateWizard(models.TransientModel):
    _name = "gn.portal.parnian.batchupdate.wizard"

    branch_id = fields.Many2one("gn.portal.parnian.translation.branch", string="Branch")
    add_to_branch = fields.Boolean(string="Add to branch")


    def action_add_to_branch(self):

        return True