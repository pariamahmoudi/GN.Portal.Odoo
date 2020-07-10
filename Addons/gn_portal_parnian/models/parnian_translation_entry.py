from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
import uuid
import datetime
from ..parnian import Parnian, ParnianTranslationProject, ParnianTranslationBranch


class ParnianTranslationEntry(models.Model):
    _name = "gn.portal.parnian.translation.entry"
    _description = 'Translation Entry'
    _order =  "id desc"
    # _inherit = ['portal.mixin', 'mail.thread',
    #             'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(string="Name", default="New")
    # key = fields.Char(string = "Key")
    guid = fields.Char(size=38, index=True, default='New')
    ar = fields.Text(string="Ar")
    fa = fields.Text(string="Fa")
    en = fields.Text(string="En")
    key1 = fields.Char(string="Key1")
    key2 = fields.Char(string="Key2")
    key3 = fields.Char(string="Key3")
    fromVersion = fields.Char(string="From Version")
    toVersion = fields.Char(string="To Version")
    tag = fields.Char(string="Tag")
    jsonData = fields.Text(string="Data")
    project_id = fields.Many2one('gn.portal.parnian.translation.project')
    file_id = fields.Many2one('gn.portal.parnian.translation.file')
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', "Draft"),
        ('request', 'Revision Requested'),
        ('inprogress', "In Progress"),
        ('final', "Final")],
        default="draft",
        string="Status")
    untranslatable = fields.Boolean(string="Untranslatable")
    size = fields.Integer(string="Size", compute='_compute_size', store=True)
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
    score = fields.Float(string="Score", default=0.0)
    last_calculated_on = fields.Datetime(string="Calculated On")
    no_reviews = fields.Integer(default=0)

    def _get_score(self):
        result = 0.5 if self.active else 1.0
        is_translated = (self.fa and self.fa != self.en) or self.untranslatable
        is_translated = result * 2 if is_translated else result
        quality_factor = 1
        if self.quality == 'perfect':
            quality_factor = 4.0
        if self.quality == 'good':
            quality_factor = 2.0
        if self.quality == 'poor':
            quality_factor = .5
        if self.quality == 'unknown':
            quality_factor = 1.0
        result = result * quality_factor
        if self.no_reviews and self.no_reviews > 0:
            result = result * self.no_reviews

        return result
    
    def recalculate(self):
        for _r in self:
            entry:ParnianTranslationEntry = _r
            entry.score = entry._get_score()
            entry.last_calculated_on = datetime.datetime.now()
        return True


    def action_final(self):
        for r in self:
            r.state = 'final'
            r.active = False
        return True

    def action_request(self):
        for r in self:
            r.state = 'request'
            r.active = True

        return True

    def action_inprogress(self):
        for r in self:
            r.state = 'inprogress'
            r.active = True

        return True

    def action_draft(self):
        for r in self:
            r.state = 'draft'
        return True

    def add_to_default_branch(self):
        branch: ParnianTranslationBranch = Parnian.get_my_default_branch(self)
        if branch:
            branch.add_entry(self)

        return True
    
    def action_like(self):
        for r in self:
            r.no_reviews = r.no_reviews+1 if r.no_reviews else 1
            r.recalculate()
        return True

    def action_dislike(self):
        for r in self:
            r.no_reviews = r.no_reviews-1 if r.no_reviews and r.no_reviews>1 else 0
            r.recalculate()
        return True


    @api.model
    def recalculate_cron(self):
        print('recalculate_cron')
        for _entry in Parnian.entries(self).search([],order="last_calculated_on",limit=1000):
            entry:ParnianTranslationEntry = _entry
            entry.recalculate()
        return True

    @api.depends('en')
    def _compute_size(self):
        for r in self:
            r.size = len(r.en) if r.en else 0

    @api.model
    def create(self, vals):
        if vals.get('guid', 'New') == 'New':
            vals['guid'] = str(uuid.uuid4())
        result = super(ParnianTranslationEntry, self).create(vals)
        return result

    def unlink(self):
        super().unlink()
        return True

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            if isinstance(name, str):
                splt = name.split('|')
                name = splt[len(splt)-1]
            result.append((rec.id, '{} : {}'.format(rec.id, name)))
        return result
