from odoo.exceptions import ValidationError
from odoo import models, fields, api

class TodoTask(models.Model):
    _name="todo_task"
    _description = "Todo Task"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_name=fields.Char()
    assign_to=fields.Many2one('res.partner')
    description=fields.Char()
    due_date=fields.Date()
    status=fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
    ])
    estimated_time=fields.Float(string="Estimated Time")
    timesheet_ids = fields.One2many(
        'account.analytic.line',
        'task_id',  # This must match the field name created above
        string="Timesheets"
    )
    total_times=fields.Float(compute='_compute_total_times',store=True)
    active=fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft', string="Status")

    @api.depends('timesheet_ids.unit_amount')
    def _compute_total_times(self):
        for rec in self:

            rec.total_times = sum(rec.timesheet_ids.mapped('unit_amount'))

    @api.constrains('total_times','estimated_time')
    def _check_total_times(self):
        for rec in self:
            if rec.total_times > rec.estimated_time:
                raise ValidationError("Total time cannot exceed estimated time")

    def action_todo_task_close(self):
         for rec in self:
             rec.write({'state':'closed'})

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.write({'state': 'pending'})

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'


    def check_task_due_date(self):
        def check_task_due_date(self):
            today = fields.Date.today()
            # Search for all tasks that are past due and not closed
            late_tasks = self.env['todo_task'].search([
                ('due_date', '<', today),
                ('state', '!=', 'closed')
            ])
            for rec in late_tasks:
                # Posts a message in the chatter to 'alarm' the user
                rec.message_post(body="Warning: This task is past its due date!")