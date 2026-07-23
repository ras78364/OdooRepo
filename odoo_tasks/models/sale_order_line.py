from odoo import api, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # def create(self,vals):
    #     for rec in vals:
    #         if 'price_unit' in rec and not self.env.user.has_group('base.group_system'):
    #             raise UserError("You do not have the required permissions to set the unit price.")
    #
    #         res = super(SaleOrderLine, self).create(vals)
    #
    #         return res

    def write(self, vals):
        unauthorized = False
        if 'price_unit' in vals and not self.env.user.has_group('base.group_system'):
            unauthorized = True
            for rec in self:
                # 1. Revert the price back to the original database value
                vals['price_unit'] = rec.price_unit
                rec.order_id.message_post(
                    body=f"Unauthorized price modification attempt by {self.env.user.name} was blocked and reverted."
                )
        res = super(SaleOrderLine, self).write(vals)

        return res



    # def _can_edit_price_unit(self):
    #     return self.env.user.has_group("base.group_system")
    #
    # def _get_original_price_unit(self):
    #     self.ensure_one()
    #     if self._origin:
    #         return self._origin.price_unit
    #     return False
    #
    # @api.onchange("price_unit")
    # def _onchange_price_unit_security(self):
    #     if self._can_edit_price_unit():
    #         return
    #     for line in self:
    #         original = line._get_original_price_unit()
    #         if original is False:
    #             continue
    #         currency = line.currency_id or line.order_id.currency_id
    #         precision = currency.decimal_places if currency else 2
    #         if float_compare(line.price_unit, original, precision_digits=precision):
    #             line.price_unit = original
    #             return {
    #                 "warning": {
    #                     "title": _("Access Denied"),
    #                     "message": _("Only the administrator can modify the unit price."),
    #                 }
    #             }
    #
    # def write(self, vals):
    #     if "price_unit" in vals and not self._can_edit_price_unit():
    #         new_price = vals["price_unit"]
    #         precision = self.env["decimal.precision"].precision_get("Product Price")
    #         for line in self:
    #             if float_compare(line.price_unit, new_price, precision_digits=precision) != 0:
    #                 raise UserError(_("Only the administrator can modify the unit price."))
    #     return super().write(vals)
