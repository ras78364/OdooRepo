from odoo.exceptions import UserError
from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_inspection_done = fields.Boolean(string="Inspection Completed", default=False)
    transfer_note=fields.Text(string="Transfer Note")
    transfer_reason = fields.Selection([
        ('branch_transfer', 'Transfer to Branch'),
        ('shortage_compensation', 'Compensate Stock Shortage'),
        ('display_setup', 'Display Setup'),
        ('inventory_correction', 'Inventory Correction')
    ], string="Reason for Transfer")

    return_reason = fields.Selection([
        ('defect', 'Defect'),
        ('wrong_quantity', 'Wrong Quantity'),
        ('wrong_product', 'Wrong Product'),
        ('damage', 'Damage'),
        ('customer_request', 'Customer Request'),
    ], string="Return Reason")
    return_note = fields.Char(string="Return Note")

    def check_transferring_reason(self):
        action = self.env['ir.actions.actions']._for_xml_id('odoo_tasks.check_transfer_wizard_action')
        action['context'] = dict(self.env.context, active_id=self.id)

        return action


    def pre_delivery_inspection(self):
        action = self.env['ir.actions.actions']._for_xml_id('odoo_tasks.pre_delivery_inspection_wizard_action')
        action['context'] = {'default_picking_id': self.id}
        return action

    @api.constrains()
    def button_validate(self):
        for picking in self:
          if picking.picking_type_code=='outgoing' and not picking.is_inspection_done:
              raise UserError("You must verify the delivery before validating.")

        return super(StockPicking,self).button_validate()


    def returned_delivery(self):
        action = self.env['ir.actions.actions']._for_xml_id('odoo_tasks.returned_delivery_wizard_action')
        action['context'] = {'default_picking_id': self.id}
        return action




