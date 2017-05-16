# -*- coding: utf-8 -*-
# AgS Cost models is designed based on the PMP 10 knowledge areas.

from datetime import timedelta
from openerp import models, fields, api

class AgsProjectCommunicationReport(models.Model):
    _name = 'ags.project.communication.report'

    name = fields.Char(compute="_compute_report_name", string="Report Name", required=True)
    type = fields.Char(compute="_compute_report_type", string="Report Type", required=True)
    
    percent_completion = fields.Float(string='Project % Complete')
    
    description = fields.Html()
    
    
    report_start_date = fields.Date(string='Report Start Date', required=True)
    report_end_date = fields.Date(string='Report End Date', required=True)
        
    project_id = fields.Many2one('ags.project', ondelete='cascade', string="Project", required=True)
 
    @api.one
    @api.depends('report_start_date', 'type')
    def _compute_report_name(self):
        
        report_name = ""
        if self.project_id:
            report_name = "<" + self.project_id.name + ">: "
        
        if self.report_start_date:
            report_name = report_name + self.report_start_date
        
        if self.type:
            report_name = report_name + " " + self.type
        
        self.name = report_name
        return
    
    @api.one
    @api.depends('project_id')
    def _compute_report_type(self):
        
        if self.project_id:
            self.type = self.project_id.report_frequency.capitalize() + " Report"
        return




class AgsProjectCommunicationTaskReport(models.Model):
    _name = 'ags.project.communication.task.report'

    name = fields.Char(compute="_compute_report_name", string="Report Name", required=True)
    type = fields.Char(compute="_compute_report_type", string="Report Type", required=True)
    
    percent_completion = fields.Float(string='Task % Complete')
    
    description = fields.Html()
    
    
    report_start_date = fields.Date(string='Report Start Date', required=True)
    report_end_date = fields.Date(string='Report End Date', required=True)
        
    project_id = fields.Many2one('ags.project', ondelete='cascade', string="Project", required=True)
    task_id = fields.Many2one('ags.project.cost.task', ondelete='cascade', string="Task", required=True)
 
    @api.one
    @api.depends('report_start_date', 'type')
    def _compute_report_name(self):
        
        report_name = ""
        if self.task_id:
            report_name = "<" + self.task_id.name + ">: "
        
        if self.report_start_date:
            report_name = report_name + self.report_start_date
        
        if self.type:
            report_name = report_name + " " + self.type
        
        self.name = report_name
        return
    
    @api.one
    @api.depends('task_id')
    def _compute_report_type(self):
        
        if self.task_id:
            self.type = self.task_id.report_frequency.capitalize() + " Report"
        return
    


    @api.onchange('project_id')
    def onchange_filter_tasks(self):
        res = {}
        if self.project_id:
            res['domain'] = {'task_id': [('project_id', '=', self.project_id.id)]}
       
        return res    







    