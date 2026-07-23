from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Adding the new field
    property_id = fields.Many2one('property')

    # Overriding the method
    def action_confirm(self):
        # We use super() to ensure the original confirmation logic still runs
        res = super(SaleOrder,self).action_confirm()

        # Your custom logic here
        print("Inside action_confirm")

        return res