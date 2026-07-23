from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    approval_status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting Approval'),
        ('approved', 'Approved')
    ], default='draft', string="Approval Status")

    approver_id=fields.Many2one('res.users',string="Approval By")
    approval_reason=fields.Char(string="Reason")



    def action_open_approval_wizard(self):
        self.ensure_one()
        # This ensures the wizard only opens if the status is actually 'waiting_approval'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Approval',
            'res_model': 'sale.approval.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }

    @api.onchange('order_line')
    def _onchange_check_margin(self):
        is_below_cost = False
        for rec in self.order_line:

            if rec.product_id and rec.price_unit < rec.product_id.standard_price:
                is_below_cost = True
                break


        if is_below_cost:
            self.approval_status = 'waiting_approval'
        else:
            self.approval_status = 'draft'




