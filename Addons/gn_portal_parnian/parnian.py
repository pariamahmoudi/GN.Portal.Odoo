
from odoo import models, fields, api
from typing import TYPE_CHECKING, Any, List, Dict
import logging
#from .models.parnian_translation_branch import ParnianTranslationBranch
if TYPE_CHECKING:
    from odoo.addons.sale.models.sale import SaleOrder
    from odoo.addons.sale.models.sale import SaleOrderLine
    from gn_portal_parnian.models.parnian_translation_project import ParnianTranslationProject
    from gn_portal_parnian.models.parnian_translation_entry import ParnianTranslationEntry
    from gn_portal_parnian.models.parnian_translation_branch import ParnianTranslationBranch
    from gn_portal_parnian.models.parnian_translation_branch import ParnianTranslationBranchLine
    from gn_portal_parnian.models.parnian_translation_file import ParnianTranslationFile
else:
    SaleOrder = models.Model
    SaleOrderLine = models.Model
    ParnianTranslationProject = models.Model
    ParnianTranslationEntry = models.Model
    ParnianTranslationFile = models.Model
    ParnianTranslationBranchLine = models.Model
    ParnianTranslationBranch = models.Model


class _parnian():

    class __constants():
        Model_Translation_Branch = "gn.portal.parnian.translation.branch"
        Entry_Model_Name = "gn.portal.parnian.translation.entry"
    constants = __constants()

    def branches(self, model: models.Model) -> ParnianTranslationBranch:
        return model.env[self.constants.Model_Translation_Branch]

    def entries(self, model: models.Model) -> ParnianTranslationEntry:
        return model.env[self.constants.Entry_Model_Name]

    def get_my_default_branch(self, model: models.Model):
        user = model.env.user
        branches = self.branches(model)
        my_branches = branches.search([('responsible', '=', user.id), ('active', '=', True)]) \
            .sorted(lambda x: x.create_date, reverse=True)
        res = my_branches[0] if len(my_branches) > 0 else branches.create({
            'responsible': user.id,
            'name': "{}'s Branch".format(user.display_name)
        })
        return res
    # ref: https://www.python-course.eu/levenshtein_distance.php
    @staticmethod
    def iterative_levenshtein(s, t, costs=(1, 1, 1)):
        """ 
            iterative_levenshtein(s, t) -> ldist
            ldist is the Levenshtein distance between the strings 
            s and t.
            For all i and j, dist[i,j] will contain the Levenshtein 
            distance between the first i characters of s and the 
            first j characters of t
            
            costs: a tuple or a list with three integers (d, i, s)
                where d defines the costs for a deletion
                        i defines the costs for an insertion and
                        s defines the costs for a substitution
        """

        rows = len(s)+1
        cols = len(t)+1
        deletes, inserts, substitutes = costs
        
        dist = [[0 for x in range(cols)] for x in range(rows)]

        # source prefixes can be transformed into empty strings 
        # by deletions:
        for row in range(1, rows):
            dist[row][0] = row * deletes

        # target prefixes can be created from an empty source string
        # by inserting the characters
        for col in range(1, cols):
            dist[0][col] = col * inserts
            
        for col in range(1, cols):
            for row in range(1, rows):
                if s[row-1] == t[col-1]:
                    cost = 0
                else:
                    cost = substitutes
                dist[row][col] = min(dist[row-1][col] + deletes,
                                    dist[row][col-1] + inserts,
                                    dist[row-1][col-1] + cost) # substitution

        for r in range(rows):
            #print(dist[r])
            pass
        
 
        return dist[row][col]


Parnian = _parnian()

