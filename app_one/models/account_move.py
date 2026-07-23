from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    # 1. Field definition
    property_id = fields.Many2one('property', string='Property')

    # 2. Method definition
    def action_do_something(self):
        # self here represents the record(s) the button was clicked on
        print(self, "inside action_do_something")
        # Example: you can access the property_id now
        for record in self:
            if record.property_id:
                print(f"Working on property: {record.property_id.name}")