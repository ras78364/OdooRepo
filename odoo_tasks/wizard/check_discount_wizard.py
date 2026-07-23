from odoo import api, fields, models, tools

class check_discount_wizard(models.TransientModel):
    _name = 'check.discount.reason'
    _description = 'Wizard to check discount reason'

    order_id = fields.Many2one('sale.order')
    discount = fields.Float(string="Discount")
    discount_reason = fields.Char(string='Discount Reason')


    def action_confirm_discount(self):

        for rec in self:
            if rec.discount > 15:
                rec.order_id.write({'state': 'waiting_approval'})
                msg = f"Discount of {rec.discount}% is too high (Limit: 15%), the state is now waiting approval from the manager."
                rec.order_id.message_post(body=msg)

        return {'type': 'ir.actions.act_window_close'}












