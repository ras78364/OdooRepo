from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'Odoo Users'


    warehouse_ids=fields.Many2many(
        'stock.warehouse',
        'user_warehouse_rel',
        'user_id',
        'warehouse_id',
        string='Allowed Warehouses'
    )



