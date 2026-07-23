from odoo.exceptions import ValidationError, UserError
from odoo import fields, models, api


class check_returned_deliveries_wizard(models.TransientModel):
    _name = 'check.returned.deliveries.wizard'
    _description = 'Check Returned Deliveries Wizard'

    picking_id = fields.Many2one('stock.picking')

    return_reason=fields.Selection([
        ('defect','Defect'),
        ('wrong_quantity','Wrong Quantity'),
        ('wrong_product','Wrong Product'),
        ('damage','Damage'),
        ('customer_request','Customer Request'),
    ])

    return_note=fields.Char('Return Note')

    def confirm_returned_delivery(self):
        for rec in self:
            if not rec.return_reason:
                raise UserError("You must select a return reason.")
            if rec.picking_id:
                rec.picking_id.write({
                    'return_reason': rec.return_reason,
                    'return_note': rec.return_note,
                })
                selection_dict = dict(rec._fields['return_reason'].selection)
                reason_display = selection_dict.get(rec.return_reason, rec.return_reason)
                note_text = rec.return_note or ''
                message = f"Return reason: {reason_display}, Note: {note_text}"
                rec.picking_id.message_post(body=message, subject='Return reason')
                rec.picking_id.write({'state': 'draft'})

        return {'type': 'ir.actions.act_window_close'}






