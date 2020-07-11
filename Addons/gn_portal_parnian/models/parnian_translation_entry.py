from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List
import uuid
import datetime
from ..parnian import Parnian, ParnianTranslationProject, ParnianTranslationBranch


class ParnianTranslationEntry(models.Model):
    _name = "gn.portal.parnian.translation.entry"
    _description = 'Translation Entry'
    _order = "id desc"
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
        ('acceptable', "Acceptable"),
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
    no_likes = fields.Integer(default=0, string="Likes")
    no_dislikes = fields.Integer(default=0, string="Dislikes")

    def _get_score(self):
        result = 0.5 if self.active else 1.0
        is_translated = (self.fa and self.fa != self.en) or self.untranslatable
        is_translated = result * 2 if is_translated else result
        quality_factor = 1
        if self.no_likes - self.no_dislikes > 0:
            self.quality = 'acceptable'
        if self.no_likes - self.no_dislikes > 2:
            self.quality = 'good'
        if self.no_likes - self.no_dislikes > 4:
            self.quality = 'perfect'
        if self.no_likes - self.no_dislikes < 0:
            self.quality = 'poor'

        if self.quality == 'perfect':
            quality_factor = 4.0
        if self.quality == 'good':
            quality_factor = 2.0
        if self.quality == 'poor':
            quality_factor = 0.4
        if self.quality == 'acceptable':
            quality_factor = 1.0

        if self.quality == 'unknown':
            quality_factor = .8

        result = result + self.no_likes * 1
        result = result - self.no_dislikes * 1
        result = result * quality_factor
        if self.no_reviews and self.no_reviews > 0:
            result = result * self.no_reviews*.4

        return result

    def get_nearest(self, target, en=False, limit=10):
        str_target: str = target
        filter = []
        result = False

        def sort_disatnce(d):
            return d.get('distance', 1000)

        def sort_len(w):
            return len(w)

        def add_word(w):
            if len(w) < 3:
                return
            if len(filter) > 0:
                filter.insert(0, '|')
            if en:
                filter.append(('en', 'like', w))
            else:
                filter.append(('fa', 'like', w))
            return True
        if target and len(target) > 0:
            words = str_target.split(' ')
            words.sort(key=sort_len, reverse=True)
            max_len = 0
            min_len = 10000
            sum_len = 0
            for word in words:
                max_len = len(word) if len(word) > max_len else max_len
                min_len = len(word) if len(word) < min_len else min_len
                sum_len = sum_len+1
            avg_len = sum_len/len(words)
            filter_items_count = 0
            min_filter_items = 1
            max_filter_items = 10
            for word in words:
                if len(word) >= avg_len and filter_items_count < max_filter_items:
                    add_word(word)
                    filter_items_count = filter_items_count+1
                if len(word) < avg_len and filter_items_count < min_filter_items:
                    add_word(word)
                    filter_items_count = filter_items_count+1

            
            
            #acrchive = ['|', ('active', '=', True), ('active', '=', False)]
            #filter.append(acrchive)
            #_items = self.search([('fa','like','garbage'), '|',('active', '=', True), ('active', '=', False)])
            filter.append('|')
            filter.append(('active','=',True))
            filter.append(('active','=',False))
            items = self.search(filter, limit=50)
            distances = []
            for i in items:
                entry: ParnianTranslationEntry = i
                # pylint: disable=no-member
                # if entry.id != self.id:
                if en:
                    dist = Parnian.iterative_levenshtein(target, entry.en)
                else:
                    dist = Parnian.iterative_levenshtein(target, entry.fa)

                distances.append({
                    'distance': dist,
                    'entry': entry
                })
            distances.sort(key=sort_disatnce)
            result = distances
            if len(result) > limit:
                result = result[:limit]

        return result

    def recalculate(self):
        for _r in self:
            entry: ParnianTranslationEntry = _r
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

            entry: ParnianTranslationEntry = r
            # entry.get_nearest(entry.fa)
            entry.no_likes = entry.no_likes+1 if entry.no_likes else 1
            entry.no_reviews = entry.no_reviews+1
            entry.recalculate()
        return True

    def action_dislike(self):
        for r in self:
            entry: ParnianTranslationEntry = r
            entry.no_dislikes = entry.no_dislikes+1 if entry.no_dislikes else 1
            entry.no_reviews = entry.no_reviews+1
            entry.recalculate()
        return True

    @api.model
    def recalculate_cron(self):
        print('recalculate_cron')
        for _entry in Parnian.entries(self).search([], order="last_calculated_on", limit=1000):
            entry: ParnianTranslationEntry = _entry
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
