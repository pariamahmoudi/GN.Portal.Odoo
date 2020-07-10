from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
import uuid
from ..parnian import Parnian


if TYPE_CHECKING:
    from gn_imports import ParnianTranslationProject
    from gn_imports import ParnianTranslationEntry
else:
    ParnianTranslationProject = models.Model
    ParnianTranslationEntry = models.Model


class ParnianTranslationBranch(models.Model):
    _name = "gn.portal.parnian.translation.branch"
    _description = 'Translation Branch'
    # _inherit = ['portal.mixin', 'mail.thread',
    #             'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(default="noname")
    line_ids = fields.One2many(
        comodel_name="gn.portal.parnian.translation.branch.line",
        inverse_name="branch_id")
    guid = fields.Char(size=38, index=True, default='New')

    responsible = fields.Many2one("res.users", string='Responsible')
    due_date = fields.Date(string="Due Date")
    active = fields.Boolean(default=True)


    state = fields.Selection([
        ('draft', "Draft"),
        ('inprogress', "In Progress"),
        ('submitted', "Submitted"),
        ('committed',"Committed"),
        ], 
        default="draft", 
        string="Status")

    def name_get(self):
        result = []
        for rec in self:
            name = '' if rec.name=='noname' else rec.name
            result.append((rec.id, '#{} : {}'.format(rec.id, name)))
        return result

    def add_entry(self, entry: ParnianTranslationEntry):
        result = False

        if entry:
            result = self.line_ids.filtered(lambda x: x.id == entry.id)
            if not result:
                result = self.env["gn.portal.parnian.translation.branch.line"].create({
                    # pylint: disable=no-member
                    'branch_id':self.id,
                    'entry_id': entry.id,
                    'fa': entry.fa,
                    'backup':entry.fa,
                    'en':entry.en,
                    'ar':entry.ar
                })
            if result:
                result.state="inprogress"
                result.active=True
        
        return result

    def commit(self):
        for _line in self.line_ids:
            line:ParnianTranslationBranchLine = _line
            entry:ParnianTranslationEntry = line.entry_id
            entry.fa = line.fa
            entry.no_reviews = entry.no_reviews+1 if entry.no_reviews else 1
            line.committed = True
            entry.action_final()
    
    def uncommit(self):
        if self.state in ('committed','final'):
            for _line in self.line_ids:
                line:ParnianTranslationBranchLine = _line
                entry:ParnianTranslationEntry = line.entry_id
                if entry:
                    if entry.fa==line.fa:
                        entry.fa = line.backup
                    entry.action_inprogress()
                line.committed = False

    def action_draft(self):
        self.state = 'draft'
        return True

    def action_inprogress(self):
        self.state ='inprogress'
        return True

    def action_submit(self):
        for r in self:
            r.state = 'submitted'
        return True

    def action_commit(self):
        for _branch in self:
            branch:ParnianTranslationBranch = _branch
            branch.state ='committed'
            branch.commit()
            branch.active=False
        return True
    
    def action_undo(self):
        for _branch in self:
            branch:ParnianTranslationBranch = _branch
            branch.uncommit()
            branch.active= True
            branch.state ="inprogress"

    def action_finalize(self):
        for _branch in self:
            branch:ParnianTranslationBranch = _branch
            for _line in branch.line_ids:
                line:ParnianTranslationBranchLine = _line
                line.entry_id.fa = line.fa
                line.entry_id.action_final()
            branch.state ='final'
            branch.active = False
        return True


    def action_cancel(self):
        for _branch in self:
            branch:ParnianTranslationBranch = _branch
            branch.uncommit()
            branch.active=True
            branch.state="inprogress"

        return True



    @api.model
    def create(self, vals):
        if vals.get('guid', 'New') == 'New':
            vals['guid'] = str(uuid.uuid4())
        vals['responsible'] = self.env.user.id
        result = super(ParnianTranslationBranch, self).create(vals)
        
        return result


class ParnianTranslationBranchLine(models.Model):
    _name = "gn.portal.parnian.translation.branch.line"
    _description = "Translation Branch Line"
    _order="id desc"

    branch_id = fields.Many2one(
        "gn.portal.parnian.translation.branch", string="Branch")
    entry_id = fields.Many2one(
        "gn.portal.parnian.translation.entry", string="Entry")
    fa = fields.Text("Farsi")
    en = fields.Text("English")
    ar = fields.Text("Arabic")
    backup = fields.Text("Backup")
    committed = fields.Boolean("Committed")
    is_changed=fields.Boolean("Change",compute="_compute_changed")

    @api.depends('fa')
    def _compute_changed(self):
        for r in self:
            r.is_changed = r.fa and r.fa!=r.backup





