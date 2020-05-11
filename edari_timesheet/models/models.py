# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class edari_timesheet(models.Model):
#     _name = 'edari_timesheet.edari_timesheet'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class edari_timesheet(models.Model):
    _inherit = 'account.analytic.line'

    contract_id = fields.Many2one('hr.contract', 'Contract', domain=[('state', '=', 'open')])