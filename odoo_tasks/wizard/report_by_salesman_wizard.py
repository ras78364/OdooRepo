from odoo import models, fields
from odoo.exceptions import UserError

class ReportBySalesmanWizard(models.TransientModel):
    _name='report.by.salesman.wizard'
    _description = 'Report by Salesman Wizard'

    salesperson_id=fields.Many2one('res.users',string='Salesperson')
    start_date=fields.Datetime(string='Start Date')
    end_date=fields.Datetime(string='End Date')

    def action_print_report(self):
        self.ensure_one()

        # Grab the active IDs directly from the list view context
        active_ids = self.env.context.get('active_ids', [])

        # Browse the exact records ticked in the list view
        records = self.env['sale.order'].browse(active_ids)

        data = {
            'form': {
                'salesperson_id': self.salesperson_id.id if self.salesperson_id else False,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'sale_order_ids': active_ids,
            }
        }   

        # Pass the browsed records directly to the report action
        return self.env.ref('odoo_tasks.report_by_salesman').report_action(records, data=data)