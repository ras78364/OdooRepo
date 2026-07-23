from odoo.exceptions import UserError
from odoo import fields, models


class CheckInvoiceCancellation(models.TransientModel):
    _name = 'check.invoice.cancellation'
    _description = 'Check Invoice Cancellation'


    move_id = fields.Many2one('account.move', string="Invoice")
    Invoice_cancellation_reason=fields.Selection([
        ('data_entry_error','Data Entry Error'),
        ('duplicate_issuance','Duplicate Issuance'),
        ('product_return','Product Return'),
        ('negotiated_price_adjustments','Negotiated Price Adjustments'), ],string="Reason for Cancellation")


    def action_confirm_cancellation(self):
        for rec in self:
            if not rec.Invoice_cancellation_reason:
                raise UserError("Please enter a valid cancellation reason")

            else:
                rec.move_id.write({'state':'cancel'})

        return {'type': 'ir.actions.act_window_close'}







