
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


Parnian = _parnian()
