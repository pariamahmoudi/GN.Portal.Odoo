from odoo import models, fields, api
#from typing import TYPE_CHECKING, Any, List
# pylint: disable=unused-wildcard-import
from ..parnian import *


class BatchUpdateWizard(models.TransientModel):
    _name = "gn.portal.parnian.batchupdate.wizard"
    _logger = logging.getLogger(__name__)
    branch_id = fields.Many2one("gn.portal.parnian.translation.branch", string="Branch")
    add_to_branch = fields.Boolean(string="Add to branch")
    update_priority = fields.Boolean(string="Update Priority")
    update_quality = fields.Boolean(string="Update Quality")
    update_finalize = fields.Boolean()
    update_untranslatable = fields.Boolean()
    quality = fields.Selection([
        ('unknown', "Unknwon"),
        ('poor', "Poor"),
        ('good', "Good"),
        ('perfect', "Perfect")
        ], 
        default="unknown", 
        string="Quality")
    priority = fields.Selection([
        ('medium', "Medium"),
        ('high', "Heigh"),
        ('low', "Low"),
        ], 
        default="medium", 
        string="Priority")


    def action_update_priority(self):
        return True

    def action_batch_update(self):
        entry_ids = self.env.context.get("entry_ids",False)
        branch:ParnianTranslationBranch =  self.branch_id
        if entry_ids:
            entries = Parnian.entries(self).browse(entry_ids)
            for _entry in entries:
                entry:ParnianTranslationEntry = _entry
                #entry.fa = "FAFA"

                if self.update_priority and self.priority:
                    entry.priority = self.priority
                if self.update_quality and self.quality:
                    entry.quality = self.quality
                if self.update_finalize:
                    entry.action_final()
                if self.add_to_branch:
                    branch = branch if branch else Parnian.branches(self).create({
                        'name':'noname'
                    })
                    if branch:
                        branch.add_entry(entry)
                entry.recalculate()
        return True