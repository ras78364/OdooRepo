from odoo import models, fields, api

class ApprovalWizard(models.TransientModel):
    _name = 'sale.approval.wizard'
    _description = 'Approval Wizard'

    order_id = fields.Many2one('sale.order', string="Order")
    reason=fields.Char(string='Reason')

    def approve(self):
     if self.order_id:
       self.order_id.write({
            'approval_status': 'approved',
            'approver_id': self.env.user.id,
            'approval_reason': self.reason,
            'state': 'sale',  # Optional: You likely want to move the order to the next stage
        })
     return {'type': 'ir.actions.act_window_close'}
