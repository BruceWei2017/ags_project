# -*- coding: utf-8 -*-
# AgS Cost models is designed based on the PMP 10 knowledge areas.

from datetime import timedelta
from openerp import models, fields, api
from adodbapi.adodbapi import Date

class AgsProjectCostTask(models.Model):
    _name = 'ags.project.cost.task'

    name = fields.Char(string="Task Name", required=True)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High')], 'Priority', index=True, default='0')
    
    actual_cost = fields.Integer(string='Activity Actual Cost')
    
    report_frequency = fields.Selection([
        ('weekly', "Weekly"),
        ('daily', "Daily"),
        ('monthly', "Monthly"),
        ('casual', "Casually"),
    ], default="weekly")        
    
    state = fields.Selection([
        ('new', "New"),
        ('suspend', "Suspend"),
        ('ongoing', "Ongoing"),
        ('completion', "Completion"),
    ], default='new', compute="_compute_state")
    
    percent_complete = fields.Float(compute='_compute_percent_complete', string ="Task % Complete")
    
    description = fields.Text()
    
    scope_id = fields.Html(string="Scope Statement")
    
    assign_id = fields.Many2one('res.users',
        string='Assigned to',
        default=lambda self: self.env.uid,
        index=True, track_visibility='always')
    
    plan_start_date = fields.Date(string='Plan Start Date')
    plan_end_date = fields.Date(string='Plan End Date')
    
    deliverables = fields.Char(string="Task Deliverables", required=True)
    
    actual_start_date = fields.Date(string='Actual Start Date')
    actual_end_date = fields.Date(string='Actual End Date')
        
    project_id = fields.Many2one('ags.project',
         ondelete='cascade', string="Project", default=lambda self: self.env.context.get('default_project_id'), 
         index=True,required=True)

    activity_id = fields.Many2one('ags.project.time.activity',
         ondelete='cascade', string="Activity", required=True) #domain=[('project_id', '=', 1)])    
    
    task_reports = fields.One2many('ags.project.communication.task.report', 'task_id', string="Task Reports")
    
    @api.onchange('project_id')
    def onchange_filter_activities(self):
        res = {}
        if self.project_id:
            res['domain'] = {'activity_id': [('project_id', '=', self.project_id.id)]}
       
        return res    

    @api.one
    @api.depends('task_reports')
    def _compute_percent_complete(self):
        
        self.percent_complete = 0       
        if self.task_reports:
            self.percent_complete = self.task_reports.search([], order="report_end_date desc", limit=1).percent_completion
        return     
    
    
    @api.one
    @api.depends('percent_complete')
    def _compute_state(self):
              
        if self.percent_complete >= 100:
            self.state = "completion"
        return 
    
       
    @api.one
    @api.depends('plan_start_date', 'plan_end_date', 'actual_start_date', 'actual_end_date')
    def _compute_task_actual_cost(self):
           
        self.actual_cost = 0;
        
        if self.actual_start_date and self.actual_end_date:
            self.actual_cost = self.actual_end_date - self.actual_start_date + 1
            return
        
        if self.plan_start_date and self.plan_start_date:
            #simple but not actual cost
            self.actual_cost = self.plan_end_date - self.plan_start_date + 1
            return
        
        return     
