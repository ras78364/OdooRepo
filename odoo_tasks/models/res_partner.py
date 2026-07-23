from odoo import models, fields, api
from odoo.exceptions import ValidationError


class res_partner(models.Model):
    _inherit = 'res.partner'
    _description = 'res partner'

    client_phone = fields.Char(string='Customer Phone')
    internal_client_code = fields.Char(string='Customer Code')


    def display_partner_orders(self):
        action=self.env['ir.actions.actions']._for_xml_id('odoo_tasks.partner_orders_action')
        view_id=self.env.ref('sale.sale_order_list_upload').id
        action['domain']=[('partner_id','=', self.id)]
        action['views']=[[view_id,'list']]
        action['context']={'default_partner_id': self.id}
        return action








