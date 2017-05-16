# -*- coding: utf-8 -*-
# AgS Time models is designed based on the PMP 10 knowledge areas.

from datetime import timedelta
from openerp import models, fields, api

class AgsProjectTimeMilestone(models.Model):
    _name = 'ags.project.time.milestone'

    name = fields.Char(string="Milestone Name", required=True)

    type = fields.Selection([
        ('CPT', "Contract Payment Point"),
        ('IMT', "Internal Management Point"),
    ], string="Milestone Type", required=True)
    
    
    plan_end_date = fields.Date(string='Plan End Date')
    
    deliverables = fields.Char(string="Deliverables", required=True)
    

    actual_end_date = fields.Date(string='Actual End Date')
  
    project_id = fields.Many2one('ags.project', ondelete='cascade', string="Project", index=True,required=True)
  

    
    
class AgsProjectTimePhase(models.Model):
    _name = 'ags.project.time.phase'

    name = fields.Char(string="Phase Name", required=True)
     
    state = fields.Selection([
        ('new', "New"),
        ('suspend', "Suspend"),
        ('ongoing', "Ongoing"),
        ('completion', "Completion"),
    ], default='new')
    
    plan_start_date = fields.Date(string='Plan Start Date', required=True) 
    plan_end_date = fields.Date(string='Plan End Date', required=True)
    
    
    actual_start_date = fields.Date(string='Actual Start Date')
    actual_end_date = fields.Date(string='Actual End Date')
    
    phase_activities = fields.One2many('ags.project.time.activity', 'phase_id', string="Phase Activities")    
        
    project_id = fields.Many2one('ags.project', string='Project')
    
    

    
    
    
    
class AgsProjectTimeActivity(models.Model):
    _name = 'ags.project.time.activity'

    name = fields.Char(string="Activity Name", required=True)
    description = fields.Text()
    
    color = fields.Integer()

    plan_start_date = fields.Date(string='Plan Start Date') 
    plan_end_date = fields.Date(string='Plan End Date')
    
    estimate_cost = fields.Integer(string='Estimate Cost', help="The activity cost estimated by project manager and experts.")
    actual_cost = fields.Integer(string='Actual Cost', help="The activity actual cost calculated by tasks cost.")
    
    actual_start_date = fields.Date(string='Actual Start Date')
    actual_end_date = fields.Date(string='Actual End Date')
    
    actual_cost = fields.Integer(compute="_compute_activity_actual_cost", string='Activity Actual Cost', help="The activity actual cost calculated by the Task cost summary.")
   
        
    project_id = fields.Many2one('ags.project', string='Project', required=True)     
    
    phase_id = fields.Many2one('ags.project.time.phase',
         ondelete='cascade', string="Phase", required=True)      

    activity_tasks = fields.One2many('ags.project.cost.task', 'activity_id', string="Activity Tasks")
    
    
    
    @api.one
    @api.depends('activity_tasks')
    def _compute_activity_actual_cost(self):
        
        self.actual_cost = 0       
        for atk in self.activity_tasks:
            if atk.actual_cost:
                self.actual_cost = self.actual_cost + atk.actual_cost      
        return     


    @api.onchange('project_id')
    def onchange_filter_phases(self):
        res = {}
        if self.project_id:
            res['domain'] = {'phase_id': [('project_id', '=', self.project_id.id)]}
       
        return res    

    