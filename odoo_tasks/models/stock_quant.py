from odoo.exceptions import UserError
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockQuant(models.Model):
    _inherit = "stock.quant"
    _description = "Stock Quant"

    inventory_reason=fields.Selection([
        ('counting difference','Counting Difference'),
        ('damage','Damage'),
        ('lost','Lost'),
        ('system correction','System Correction'),

    ])
    my_custom_quantity = fields.Float(string="New Counted Qty")

    state = fields.Selection([
        ('draft', 'Draft'),  # Initial state: Count is recorded but not submitted
        ('waiting_approval', 'Waiting Approval'),  # Large difference detected: Waiting for manager
        ('approved', 'Approved'),  # Manager reviewed and cleared the difference
        ('rejected', 'Rejected'),  # Manager disagreed; adjustment must be re-counted
        ('done', 'Done')  # Adjustment applied to the stock levels
    ], string="Approval Status", default='draft')




    @api.constrains('inventory_quantity','inventory_diff_quantity','quantity')
    def check_stock_quantity(self):
        threshold = float(
            self.env['ir.config_parameter'].sudo().get_param('stock.inventory_threshold', default=5.0))
        for rec in self:
            current = rec.quantity
            counted = rec.inventory_quantity
            diff = counted - current
            if abs(diff)>threshold:
                rec.write({'state': 'waiting_approval'})
            else:
                rec.write({'state': 'done'})


    # @api.constrains('inventory_quantity','inventory_reason')
    # def check_inventory_adjustment(self):
    #     for rec in self:
    #         if rec.inventory_quantity != rec.quantity:
    #          if not rec.inventory_reason:
    #             raise ValidationError("Please select inventory reason")



    def action_apply_inventory(self):
        for rec in self:
            if float(rec.inventory_quantity) != float(rec.quantity):
                if not rec.inventory_reason:
                    raise ValidationError(f"Missing reason for {rec.product_id.display_name}")

            diff = rec.inventory_quantity - rec.quantity
            if abs(diff) >= 40:
                if rec.state != 'approved':
                    # Only update state if not already approved
                    rec.write({'state': 'waiting_approval'})
                    raise UserError(
                        f"Adjustment for {rec.product_id.display_name} is too large (>40). Manager approval is required!")
            else:
                # If it's a small adjustment, mark as done
                rec.write({'state': 'done'})

            # 3. If all checks pass, apply the inventory ONCE
        return super(StockQuant, self).action_apply_inventory()


    def action_approve(self):
        for rec in self:
         rec.state = 'approved'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'




