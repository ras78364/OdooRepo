from odoo import models


class ReportBySalesman(models.AbstractModel):
    _name = 'report.odoo_tasks.report_by_salesman_template'
    _description = 'Salesman Report'


    def _get_report_values(self, docids, data=None):
            data = data or {}
            form = data.get('form', {})

            salesperson_id = form.get('salesperson_id')
            start_date = form.get('start_date')
            end_date = form.get('end_date')
            sale_order_ids = form.get('sale_order_ids', [])

            # Read directly from sale_order_ids if passed, otherwise fall back to docids
            if sale_order_ids:
                orders = self.env['sale.order'].browse(sale_order_ids)
            else:
                orders = self.env['sale.order'].browse(docids)

            salesperson = self.env['res.users'].browse(salesperson_id) if salesperson_id else self.env['res.users']

            return {
                'doc_ids': docids,
                'doc_model': 'sale.order',
                'docs': orders,
                'data': data,
                'salesperson': salesperson,
                'start_date': start_date,
                'end_date': end_date,
            }