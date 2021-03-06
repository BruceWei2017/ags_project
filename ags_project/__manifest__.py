# -*- coding: utf-8 -*-
{
    'name': "AgS Project",
    'summary': 'Projects, Tasks, Issues, Reports',
    'description': """
AgS Project
====================================================

AgS (All get Success) Project provides a tool based on the project management framework widely recognized by the industry.

This application enables a group of people to intelligently and efficiently manage projects' different area, including scope, quality, schedule and cost etc. All the business elements of this application is based on the industry recognized project management framework terms, like Phase, Task, Activity, Issue, BAC etc.

So, if you're a project manager especially who got certified by the PMI, you'll find it unbelievable easy to use this tool.

It will help you to manage your project whole life-cycle successfully from its initiating to closing.

AgS Project will mainly include:
-------------------------------
- Integration Management
- Scope Management
- Schedule Management
- Quality Management
- Earned Value Management

""",
    'author': "Bruce Wei",
    'website': "http://www.odoo.com",
    'category': 'Project',
    'version': '1.0',
    'depends': ['base', 'hr'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/ags_project_views.xml',
    ],
    'demo': [
        'demo.xml',
    ],
    'price': 49.99,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
}

