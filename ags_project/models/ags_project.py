# -*- coding: utf-8 -*-
# AgS Projects models is designed based on the PMP 10 knowledge areas.
from openerp import models, fields, api
from gdata.data import REQUIRED_ATENDEE




class AgsProject(models.Model):
    _name = 'ags.project'

    code = fields.Char(string="Project Code", required=True, index=True)
    name = fields.Char(string="Project Name", required=True)
    type = fields.Many2one('ags.project.type', ondelete='set null', string="Project Type", index=True,required=True)
    
    percent_complete = fields.Float(compute='_compute_percent_complete', string ="Project % Complete")
    
    description = fields.Text()
    
    department_id = fields.Many2one('hr.department', ondelete='set null', string="Department", index=True,required=True)
    
    manager_id = fields.Many2one('res.users',
        string='Project Manager',
        default=lambda self: self.env.uid,
        index=True, track_visibility='always')
    
    director_id = fields.Many2one('res.users',
        string='Project Director',
        default=lambda self: self.env.uid,
        index=True, track_visibility='always')
    
    current_phase = fields.Char(compute='_compute_current_phase', string="Current Phase", index=True,required=True, readonly=True)
   
    plan_start_date = fields.Date(string='Plan Start Date') 
    plan_end_date = fields.Date(string='Plan End Date')
    
    
    actual_start_date = fields.Date(string='Actual Start Date')
    actual_end_date = fields.Date(string='Actual End Date')
    
    
    
    
    @api.multi
    def action_initiating(self):
        self.state = 'initiating'
        
    @api.multi
    def action_planning(self):
        self.state = 'planning'

    @api.multi
    def action_doing(self):
        self.state = 'doing'
        
    @api.multi
    def action_closing(self):
        self.state = 'closing'
    
    
    
    # Cost Management
    estimate_cost = fields.Integer(string='Estimate Cost')
    budget_at_completion = fields.Integer(compute='_compute_budget_at_completion', string='Budget at Completion', readonly=True)
    #calculated by the activity cost
    actual_cost = fields.Integer(compute="_compute_project_actual_cost", string='Actual Cost', help="The project actual cost calculated by the Task cost summary.")

    
    
    project_activities = fields.One2many('ags.project.time.activity', 'project_id', string="Project Activities")
    project_tasks = fields.One2many('ags.project.cost.task', 'project_id', string="Project Tasks")
    
    # Time Management     
    project_phases = fields.One2many('ags.project.time.phase', 'project_id', string="Project Phases")
    project_milestones = fields.One2many('ags.project.time.milestone', 'project_id', string="Project Milestones")
    
    @api.one
    @api.depends('project_phases')
    def _compute_current_phase(self):
        for ps in self.project_phases:
            if ps.state == 'suspend' or ps.state == 'ongoing':
                self.current_phase = ps.name
                return
        self.current_phase = 'To Be Determined' #self.env['ags.project.time.phase'].search([('name', '=', 'To Be Determined')], limit=1).id    
       
       
    @api.one
    @api.depends('project_activities')
    def _compute_budget_at_completion(self):
        
        self.budget_at_completion = 0       
        for pas in self.project_activities:
            self.budget_at_completion = self.budget_at_completion + pas.estimate_cost      
        return     


    @api.one
    @api.depends('project_reports')
    def _compute_percent_complete(self):
        
        self.percent_complete = 0       
        if self.project_reports:
            self.percent_complete = self.project_reports.search([], order="report_end_date desc", limit=1).percent_completion
        return     
            
    
    
    @api.one
    @api.depends('project_activities')
    def _compute_project_actual_cost(self):
        
        self.actual_cost = 0       
        for pac in self.project_activities:
            if pac.actual_cost:
                self.actual_cost = self.actual_cost + pac.actual_cost      
        return    
    
    state = fields.Selection([
        ('initiating', "Initiating"),
        ('planning', "Planning"),
        ('doing', "Executing & Monitoring"),
        ('closing', "Closing"),
    ], default="initiating")
    
    
    report_frequency = fields.Selection([
        ('weekly', "Weekly"),
        ('daily', "Daily"),
        ('monthly', "Monthly"),
        ('casual', "Casually"),
    ], default="weekly")
    
    # Scope Management
    scope_statement = fields.Html(string="Scope Statement");


    # Communication Management
    project_reports = fields.One2many('ags.project.communication.report', 'project_id', string="Project Reports")


    # Quality Management
    project_issues = fields.One2many('ags.project.quality.issue', 'project_id', string="Project Issues")

    

    # Earned Value Management
    planned_value = fields.Float(compute='_compute_planned_value', string ="Planned Value");
    earned_value = fields.Float(compute='_compute_earned_value', string ="Earned Value");
    schedule_variance = fields.Float(compute='_compute_schedule_variance', string ="Schedule Variance");
    cost_variance = fields.Float(compute='_compute_cost_variance', string ="Cost Variance");


    @api.one
    @api.depends('project_activities')
    def _compute_planned_value(self):
        
        self.planned_value = 0       
        for pas in self.project_activities:
  
            if pas.plan_end_date and  fields.Date.from_string(pas.plan_end_date) <= fields.Date.from_string(fields.Date.today()):
                    self.planned_value = self.planned_value + pas.estimate_cost;
            elif pas.plan_start_date and fields.Date.from_string(pas.plan_start_date) <= fields.Date.from_string(fields.Date.today()):
                    self.planned_value = self.planned_value + pas.estimate_cost * 0.5; 
            else:
                    self.planned_value = self.planned_value           
        return 
    
    @api.one
    @api.depends('percent_complete', 'budget_at_completion')
    def _compute_earned_value(self):
        
        self.earned_value = 0;
        
        if self.budget_at_completion and self.percent_complete:
            self.earned_value = self.budget_at_completion * self.percent_complete / 100
          
        return  
    
    
    @api.one
    @api.depends('earned_value', 'planned_value')
    def _compute_schedule_variance(self):
        
        self.schedule_variance = 0       
        
        if self.planned_value and self.earned_value:
            self.schedule_variance = self.earned_value - self.planned_value
              
        return         


    @api.one
    @api.depends('earned_value', 'actual_cost')
    def _compute_cost_variance(self):
        
        self.cost_variance = 0       
        
        if self.earned_value and self.actual_cost:
            self.cost_variance = self.earned_value - self.actual_cost
              
        return

class AgsProjectType(models.Model):
    _name = 'ags.project.type'

    code = fields.Char(string="Project Type Code", required=True, index=True)
    name = fields.Char(string="Project Type Name", required=True)
    
    
    description = fields.Text()




                 
class AgsProjectIntegration(models.Model):
    _name = 'ags.project.integration'

    name = fields.Char(string="Integration Name", required=False)
    project_id = fields.Many2one('ags.project',
        ondelete='cascade', string="Project", required=True)


class AgsProjectScope(models.Model):
    _name = 'ags.project.scope'

    name = fields.Char(string="Scope Name", required=False)
    project_id = fields.Many2one('ags.project',
        ondelete='cascade', string="Project", required=True)
    
    
class AgsProjectHumanResource(models.Model):
    _name = 'ags.project.humanresource'

    name = fields.Char(string="HumanResource Name", required=False)
    project_id = fields.Many2one('ags.project',
        ondelete='cascade', string="Project", required=True)
 
 
class AgsProjectRisk(models.Model):
    _name = 'ags.project.risk'

    name = fields.Char(string="Risk Name", required=False)
    project_id = fields.Many2one('ags.project',
        ondelete='cascade', string="Project", required=True)

class AgsProjectStakeholder(models.Model):
    _name = 'ags.project.stakeholder'

    name = fields.Char(string="StakeHolder Name", required=False)
    project_id = fields.Many2one('ags.project',
        ondelete='cascade', string="Project", required=True)
    
  
        
class AgsProjectProcurement(models.Model):
    _name = 'ags.project.procurement'

    name = fields.Char(string="Procurement Name", required=False)
    project_id = fields.Many2one('ags.project',
        ondelete='cascade', string="Project", required=True)

 
    
        