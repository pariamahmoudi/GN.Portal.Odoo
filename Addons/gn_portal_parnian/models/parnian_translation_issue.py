from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
import uuid
import datetime
from ..parnian import Parnian, ParnianTranslationEntry, ParnianTranslationBranch


class ParnianTranslationIssue(models.Model):
    _name = "gn.portal.parnian.translation.issue"
    _description = 'Translation Issue'
    _order = "id desc"

    name = fields.Char(default="New")
    description = fields.Char()
    hint = fields.Char(string="Hint")
    hint_en = fields.Char(string="Hint (English)")
    
    line_ids = fields.One2many("gn.portal.parnian.translation.issue.line",inverse_name="issue_id")
    responsible = fields.Many2one("res.users",string="Responsible")
    state = fields.Selection([
        ('draft', "Draft"),
        ('submitted', "Submitted"),
        ('done', "Done")],
        string='Status', default='draft')
    branch_id = fields.Many2one("gn.portal.parnian.translation.branch",string="Branch")




    def create_branch(self):
        result = False
        if len(self.line_ids)>0:
            branch:ParnianTranslationBranch = Parnian.branches(self).create({
                'name' : "issue: {}".format(self.name),
                'branch_type':'issue',
                # pylint: disable=no-member
                'issue_id':self.id

            })
            for e in self.line_ids:
                entry:ParnianTranslationEntry = e.entry_id
                if entry:
                    branch.add_entry(entry)




        return result

    def action_submit(self):
        self.create_branch()
        self.state ='submitted'
        return True
    def action_clear(self,only_auto=True):
        for r in self.line_ids:
            if not only_auto or r.auto:
                r.unlink()
    def action_auto_add_lines(self):
        if self.hint and len(self.hint) >0:
            items = Parnian.entries(self).get_nearest(self.hint)
            if items:
                for item in items:
                    dist = item.get('distance',1000)
                    entry:ParnianTranslationEntry = item.get('entry',False)
                    if entry:
                        self.env['gn.portal.parnian.translation.issue.line'].create({
                            'issue_id':self.id,
                            'entry_id':entry.id,
                            'fa':entry.fa,
                            'en':entry.en,
                            'distance':dist,
                            'auto':True

                        })





        return True



class ParnianTranslationIssueLine(models.Model):
    _name = "gn.portal.parnian.translation.issue.line"
    _description = 'Translation Issue Line'
    issue_id = fields.Many2one("gn.portal.parnian.translation.issue", ondelete='cascade')
    auto = fields.Boolean(default=False)
    entry_id = fields.Many2one("gn.portal.parnian.translation.entry")
    fa = fields.Text(string="Fa")
    en = fields.Text(string="EN")
    distance= fields.Float(string="Distance")

