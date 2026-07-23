from odoo.exceptions import ValidationError, UserError
from odoo import fields, models, api

class Pre_delivery_inspection(models.TransientModel):
    _name = 'pre.delivery.inspection'
    _description = 'Pre_delivery_inspection'

    picking_id = fields.Many2one('stock.picking')
    check_products = fields.Boolean(string="Correct Products?")
    check_client_data = fields.Boolean(string="Client Data Correct?")
    check_packaging = fields.Boolean(string="Packaging Intact?")
    check_quantity = fields.Boolean(string="Correct Product and Quantity?")




    def confirm_delivery_inspection_action(self):
        for rec in self:
            if not(rec.check_client_data and rec.check_packaging and rec.check_products and rec.check_quantity):
                raise UserError("You must verify all items in the checklist to proceed.")

            if rec.picking_id:
                rec.picking_id.write({'is_inspection_done': True})
                if rec.picking_id.state == 'draft':
                    rec.picking_id.action_confirm()

                    # Step B: Attempt to reserve stock (moves to assigned/Ready)
                rec.picking_id.action_assign()

        return {'type': 'ir.actions.act_window_close'}