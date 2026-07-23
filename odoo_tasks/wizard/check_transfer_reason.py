from odoo.exceptions import ValidationError
from odoo import fields, models, api

class CheckTransferReason(models.TransientModel):
    _name = 'check.transfer.reason'
    _description = 'Check Transfer Reason'

    picking_id = fields.Many2one('stock.picking', string="Related Transfer")
    x_source_warehouse_id = fields.Many2one('stock.warehouse', string="Source Warehouse")
    x_dest_warehouse_id = fields.Many2one('stock.warehouse', string="Destination Warehouse")

    transfer_reason = fields.Selection([
        ('branch_transfer', 'Transfer to Branch'),
        ('shortage_compensation', 'Compensate Stock Shortage'),
        ('display_setup', 'Display Setup'),
        ('inventory_correction', 'Inventory Correction')
    ], string="Reason for Transfer")

    transfer_note = fields.Text(string="Transfer Note")


    def action_confirm_transferring(self):
        for rec in self:
            if not rec.transfer_reason:
                raise ValidationError("Action aborted: You must select a 'Reason for Transfer' before validating this movement.")
            if rec.picking_id:
                rec.picking_id.write({
                    'transfer_reason': rec.transfer_reason,
                    'transfer_note': rec.transfer_note,
                })

                # Post the reason and the note to the chatter as a message
                reason_display = dict(self._fields['transfer_reason'].selection).get(rec.transfer_reason, rec.transfer_reason)
                note_text = rec.transfer_note or ''
                message = 'Transfer reason:%s, Note:%s' % (reason_display, note_text)
                rec.picking_id.message_post(body=message, subject='Transfer reason')
        return {'type': 'ir.actions.act_window_close'}
