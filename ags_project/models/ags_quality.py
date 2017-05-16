# -*- coding: utf-8 -*-
# AgS Time models is designed based on the PMP 10 knowledge areas.

from datetime import timedelta
from openerp import models, fields, api

    
class AgsProjectQualityIssue(models.Model):
    _name = 'ags.project.quality.issue'

    name = fields.Char(string="Issue Summary", required=True)
    description = fields.Text()
    
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High')], 'Priority', index=True, default='0')
    priority_reason = fields.Char(string="High Priority Reason")

    state = fields.Selection([
        ('new', "New"),
        ('suspend', "Suspend"),
        ('ongoing', "Ongoing"),
        ('close', "Closed"),
    ], default='new')
    
    
    submit_date = fields.Date(string='Submit Date', default=fields.Date.today()) 
    submit_id = fields.Many2one('res.users',
        string='Submit By',
        default=lambda self: self.env.uid,
        index=True, track_visibility='always')
    assign_id = fields.Many2one('res.users', string='Assigned to',  index=True, required=True, track_visibility='always')
    plan_close_date = fields.Date(string='Plan Close Date', required=True)
    actual_close_date = fields.Date(compute="_compute_actual_close_date", string='Actual Close Date')
    
    
    project_id = fields.Many2one('ags.project', ondelete='cascade', string="Project", index=True,required=True)    
    
    phase_id = fields.Many2one('ags.project.time.phase', ondelete='set null', string="Phase")      


    @api.one
    @api.depends('state')
    def _compute_actual_close_date(self):
              
        if self.state == "close":
            self.actual_close_date = fields.Date.today()
        return 
    
    @api.onchange('project_id')
    def onchange_filter_phases(self):
        res = {}
        if self.project_id:
            res['domain'] = {'phase_id': [('project_id', '=', self.project_id.id)]}
       
        return res  
    