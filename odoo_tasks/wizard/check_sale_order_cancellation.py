from odoo.exceptions import UserError
from odoo import fields, models

class CheckSaleOrderCancellation(models.TransientModel):
    _name = 'check.sale.order.cancellation'
    _description = 'Wizard to check sale order cancellation'

    order_id = fields.Many2one('sale.order')
    cancel_reason = fields.Char(string='Cancellation Reason')

    def action_confirm_cancellation(self):
        for rec in self:
            if not rec.cancel_reason:
                msg = f"Please Enter a valid reason for the deletion process"
                raise UserError("You must verify all items in the checklist to proceed.")
            else:
                rec.order_id.write({'state': 'cancelled'})

            return {'type': 'ir.actions.act_window_close'}




