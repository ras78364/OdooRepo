from odoo import models, fields
from odoo.exceptions import UserError

class ReportBySalesmanWizard(models.TransientModel):
    _name='report.by.unpaid.invoice.wizard'
    _description ='report by unpaid invoice wizard'

    partner_id=fields.Many2one('res.partner',string='Customer')
    start_date=fields.Date(string='Start Date')
    end_date=fields.Date(string='End Date')

    def action_print_report(self):
        self.ensure_one()

        domain=[
            ('move_type','in',('out_invoice','out_refund')),
            ('state', '=', 'posted'),
            ('amount_residual','>',0)
        ]
        if self.partner_id:
            domain.append(('partner_id','=',self.partner_id.id))
        if self.start_date:
            domain.append(('invoice_date','>=',self.start_date))
        if self.end_date:
            domain.append(('invoice_date','<=',self.end_date))

        records = self.env['account.move'].search(domain)
        print("--- DEBUG DOMAIN ---", domain)
        print("--- FOUND RECORDS ---", records)

        if not records:
            raise UserError('No unpaid invoices match the specified criteria.')


        data={
            'form':{
                'partner_id': self.partner_id.id,
                'start_date': self.start_date,
                'end_date': self.end_date,

            }
        }

        return self.env.ref('odoo_tasks.report_by_unpaid_invoice').report_action(records, data=data)




