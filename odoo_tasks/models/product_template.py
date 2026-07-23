from odoo.exceptions import ValidationError
from odoo import fields, api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Product Template"

    requires_barcode = fields.Boolean(string="Require Barcode")

    # @api.constrains('barcode', 'requires_barcode')
    # def _check_barcode_requirement(self):
    #     for rec in self:
    #         if rec.requires_barcode and not rec.barcode:
    #             raise ValidationError("This product requires a barcode. Please enter a valid barcode before saving.")
    #
    #
    @api.model_create_multi
    def create(self, vals):
        # 1. Iterate through the list of records being created
        for rec in vals:
            # 2. Check the requirements
            if rec.get('requires_barcode') and not rec.get('barcode'):
                raise ValidationError("You MUST enter a barcode for this product.")

        # 3. Use the modern super() - no class name required!
        return super().create(vals)

    def write(self,vals):
        for rec in self:
            require=vals.get('requires_barcode', rec.requires_barcode)
            barcode=vals.get('barcode', rec.barcode)
            if require and not barcode:
                raise ValidationError("You MUST enter a barcode for this product.")
        return super().write(vals)