from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

class Property(models.Model):
    _name = "property"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Property"
    ref=fields.Char(readonly=True,default='New')
    name = fields.Char(required=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean(tracking=1)
    expected_price = fields.Float()
    selling_price = fields.Float()
    difference = fields.Float(compute='_compute_difference', store=True)
    bedrooms = fields.Integer(required=True)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    # Fixed: Changed readonly=0 to readonly=False to satisfy Odoo boolean requirements
    owner_address = fields.Char(related='owner_id.address', readonly=False)
    owner_phone = fields.Char(related='owner_id.phone', readonly=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')
    create_time=fields.Datetime(default=fields.Datetime.now())
    next_time=fields.Datetime(compute='_compute_next_time')

    # Kept as requested
    _unique_name = models.Constraint(
        'unique(name)',
        'This property name already exists!'
    )

    line_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time=rec.create_time+ timedelta(hours=6)
            else:
                rec.next_time=False


    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_difference(self):
        print("inside _compute_difference")
        for rec in self:
            rec.difference = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price and rec.expected_price < 0:
                rec.expected_price = 0.0
                return {
                    'warning': {
                        'title': 'Invalid Price',
                        'message': 'The expected price cannot be negative.',
                        'type': 'notification',
                    }
                }
        return None

    @api.constrains('bedrooms')
    def check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError("Please enter a valid number of bedrooms!")

    def action_draft(self):
        for rec in self:
            # We use 'None' or 'Initial' if the record has no previous state
            rec.create_history_record(rec.state or 'Initial', 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state or 'Initial', 'pending')
            rec.write({'state': 'pending'})

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state or 'Initial', 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state or 'Initial', 'closed')
            rec.state = 'closed'

    def check_expected_selling_date(self):
        property_ids=self.search([])
        for rec in property_ids:
         if rec.expected_selling_date and rec.expected_selling_date<fields.Date.today():
             rec.is_late = True

    def action(self):

        print(self.env['property'].search([('name','!=','Property1')]))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state,reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason':reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.line_ids],

            })

    def action_open_change_state_wizard(self):
       action=self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
       action['context']={'default_property_id':self.id}
       return action

    def action_open_related_owner(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id=self.env.ref('app_one.owner_view_form').id
        action['res_id']=self.owner_id.id
        action['views']=[[view_id,'form']]
        return action

    def get_properties(self):
        payload=dict()
        try:
         response= requests.get('http://localhost:8069/v1/properties', data=payload)
         if response.status_code == 200:
             print("successful")

         else:
             print("failed")
        except Exception as error:
            raise ValidationError(str(error))

    def property_xlsx_report(self):
        # Get all selected IDs as a comma-separated string
        active_ids = self.env.context.get('active_ids', [])
        ids_str = ",".join(map(str, active_ids))

        return {
            'type': 'ir.actions.act_url',
            'url': f'/property/excel/report/{ids_str}',
            'target': 'new'
        }


    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals)
    #     print("inside create method")
    #     return res

    # @api.model
    # def _search(self, domain, *args, **kwargs):
    #     res = super(Property, self)._search(domain, *args, **kwargs)
    #     print("Inside search method - Custom logging active")
    #     return res

    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("inside write method")
    #     return res

    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("inside unlink method")
    #     return res


class PropertyLine(models.Model):
    _name = 'property.line'
    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()