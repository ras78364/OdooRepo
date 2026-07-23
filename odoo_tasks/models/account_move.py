from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move'
    payment_info_total=fields.Float(string='Total Amount', compute='_compute_payment_summary')
    payment_info_paid=fields.Float(string='Amount Paid',compute='_compute_payment_summary')
    payment_info_residual=fields.Float(string='Amount Residual',compute='_compute_payment_summary')
    payment_info_state=fields.Char(string='Payment State',compute='_compute_payment_summary')
    partner_vat = fields.Char(related='partner_id.vat', string="Tax ID", readonly=True)
    ref= fields.Char(default='New', string='Reference', readonly=True)
    threshold=fields.Float(string="Approval Threshold", default=10000.0)
    state = fields.Selection(
        selection_add=[('pending_approval', 'Waiting for Approval'), ('approved', 'Approved')],
        ondelete={
            'pending_approval': lambda recs: recs.write({'state': 'draft'}),
            'approved': lambda recs: recs.write({'state': 'draft'})
        })

    status_in_payment = fields.Selection(
        selection_add=[('pending_approval', 'Waiting for Approval'), ('approved', 'Approved')],
        ondelete={
            'pending_approval': lambda recs: recs.write({'status_in_payment': 'draft'}),
            'approved': lambda recs: recs.write({'status_in_payment': 'draft'})
        })

    @api.model_create_multi
    def create(self, vals_list):
        # Prevent non-admin users from setting the payment term on creation
        for vals in vals_list:
            if 'invoice_payment_term_id' in vals and not self.env.user.has_group('base.group_system'):
                
                raise UserError("You do not have the required permissions to set payment terms.")
        res = super(AccountMove, self).create(vals_list)
        for rec in res:
            if rec.ref == 'New':
                rec.ref = self.env['ir.sequence'].next_by_code('Bill_seq')
        return res

    def action_post(self):
        if not self.env.user.has_group('odoo_tasks.group_accounting_cashier'):
            raise UserError("Only administrators can post invoices.")

        if not self.partner_vat:
            raise UserError("The Tax ID is required for the customer")

        pending_approval = self.filtered(lambda rec: rec.amount_total > rec.threshold and rec.state != 'posted')
        if pending_approval:
            pending_approval.write({'state': 'pending_approval'})
            return True

        return super(AccountMove, self).action_post()


    def action_approve(self):
        for rec in self:
            rec.write({'state': 'approved'})



    @api.depends(
        'amount_total',
        'amount_residual',
        'payment_state',
        'matched_payment_ids',
        'matched_payment_ids.amount',
        'matched_payment_ids.state',
        'reconciled_payment_ids',
    )
    def _compute_payment_summary(self):
        for rec in self:
            currency = rec.currency_id or rec.company_id.currency_id
            linked_payments = rec.matched_payment_ids.filtered(
                lambda p: p.state == 'paid'
            )
            if linked_payments:
                paid = sum(linked_payments.mapped('amount'))
            else:
                paid = rec.amount_total - rec.amount_residual

            residual = rec.amount_total - paid
            if currency.compare_amounts(residual, 0) < 0:
                residual = 0.0

            # Custom state based on linked payments, not only accounting residual.
            if currency.is_zero(rec.amount_total) and not paid:
                state = dict(self._fields['payment_state'].selection).get(rec.payment_state)
            elif currency.compare_amounts(paid, rec.amount_total) >= 0:
                state = 'Paid'
            elif currency.compare_amounts(paid, 0) > 0:
                state = 'Partially Paid'
            else:
                state = dict(self._fields['payment_state'].selection).get(rec.payment_state)

            rec.payment_info_total = rec.amount_total
            rec.payment_info_paid = paid
            rec.payment_info_residual = residual
            rec.payment_info_state = state

    def _invoice_cancellation_reason(self):
        action=self.env['ir.actions.actions']._for_xml_id('odoo_tasks.check_invoice_cancellation_reason_action')
        action['context']={'default_move_id': self.id}

        return action

    def action_report_by_unpaid_invoice_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('odoo_tasks.action_report_by_unpaid_invoice_wizard')
        action['context'] = {'default_move_id': self.id}

        return action

    def action_register_payment(self):
        if not self.env.user.has_group('odoo_tasks.group_accounting_cashier'):
            raise UserError("You do not have the required permissions to register payments.")
        return super().action_register_payment()

    # def action_force_register_payment(self):
    #     if not self.env.user.has_group('odoo_tasks.group_accounting_cashier'):
    #         raise UserError("You do not have the required permissions to register payments.")
    #     return super().action_force_register_payment()

    def write(self, vals):
        # Prevent non-admin users from changing the payment term
        if 'invoice_payment_term_id' in vals and not self.env.user.has_group('base.group_system'):
            raise UserError("You do not have the required permissions to modify payment terms.")
        return super(AccountMove, self).write(vals)





















