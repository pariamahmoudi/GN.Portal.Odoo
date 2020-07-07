from typing import TYPE_CHECKING, Any,List, Dict
if TYPE_CHECKING:
    from odoo import models, fields, api
    from odoo.addons.sale.models.sale import SaleOrder
    from odoo.addons.sale.models.sale import SaleOrderLine
else:
    SaleOrder = models.Model
    SaleOrderLine = models.Model

