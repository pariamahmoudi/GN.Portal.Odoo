from typing import TYPE_CHECKING, Any,List, Dict
if TYPE_CHECKING:
    from odoo import models, fields, api
    from odoo.addons.sale.models.sale import SaleOrder
    from odoo.addons.sale.models.sale import SaleOrderLine
    from gn_portal_parnian.models.parnian_translation_project import ParnianTranslationProject
    from gn_portal_parnian.models.parnian_translation_entry import ParnianTranslationEntry
    from gn_portal_parnian.models.parnian_translation_branch import ParnianTranslationBranch
    from gn_portal_parnian.models.parnian_translation_file import ParnianTranslationFile
else:
    SaleOrder = models.Model
    SaleOrderLine = models.Model
    ParnianTranslationProject = models.Model
    ParnianTranslationEntry = models.Model
    ParnianTranslationFile = models.Model
    ParnianTranslationBranch = models.Model

