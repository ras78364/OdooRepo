from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    qty_to_order = fields.Float(
        string='Difference',
        compute='_compute_qty_to_order'
    )

    @api.depends('qty_available', 'reordering_min_qty')
    def _compute_qty_to_order(self):
        for product in self:
            # Displays the deficit clearly
            product.qty_to_order = max(0, product.reordering_min_qty - product.qty_available)