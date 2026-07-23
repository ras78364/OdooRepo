from odoo import models


class ReportBySalesman(models.AbstractModel):
    _name = 'report.odoo_tasks.report_by_salesman_template'
    _description = 'Salesman Report'


    def _get_report_values(self, docids, data=None):

        form_data=data.get('form',{}) if data else {}
        start_date=form_data.get('start_date')
        end_date=form_data.get('end_date')
        partner_id=form_data.get('partner_id')

        docs=self.env['account.move'].browse(docids)

        return{
            'doc_ids': docids,
            'doc_model': 'account.move',
            'start_date': start_date,
            'end_date': end_date,
            'partner_id': self.env['res.partner'].browse(partner_id) if partner_id else False,
        }

