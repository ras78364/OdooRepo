from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Sale_Order(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'



    partner_id=fields.Many2one('res.partner')
    client_phone = fields.Char(string='Customer Phone',related='partner_id.client_phone', store=True)
    client_vat = fields.Char(string='Tax Id',related='partner_id.vat', store=True)
    internal_client_code=fields.Char(string='Customer Code',related='partner_id.internal_client_code', store=True)
    #is_approved = fields.Boolean()
    # Add custom statuses to the existing sale.order.state field instead of overriding it
    state = fields.Selection(selection_add=[
        ('waiting_approval', 'Waiting Approval'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='draft', string='Status')


    @api.constrains('partner_id','client_phone', 'client_vat', 'internal_client_code')
    def _check_customer_data(self):
        for rec in self:
            if rec.partner_id:
             if not rec.client_phone or not rec.client_vat or not rec.internal_client_code:
                raise ValidationError('Customer Phone, VAT and Customer Code are required.')


    def _check_discount_reason(self):
        action=self.env['ir.actions.actions']._for_xml_id('odoo_tasks.check_discount_reason_action')
        action['context']={'default_order_id': self.id}

        return action

    def _check_order_cancellation_reason(self):
        # Return the act_window action to open the cancellation wizard
        action = self.env['ir.actions.actions']._for_xml_id('odoo_tasks.check_cancellation_reason_action')
        action['context'] = {'default_order_id': self.id}

        return action

    def action_report_by_salesman_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('odoo_tasks.action_report_by_salesman_wizard')
        action['context'] = {'default_order_id': self.id}

        return action




    def action_approve(self):
        for rec in self:
            rec.write({'state':'sale'})
            self.message_post(body="Order approved by Manager.")
        return True

