# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class JobsExtension(models.Model):
	_inherit='hr.job'

	customer = fields.Many2one('res.partner')

	def so_smart_button(self):
		print ('XXXXXXXXXXXXXXXXXXXXXXXX')
		rec = self.env['sale.order'].search([('job_pos','=',self.id)]).ids

		for x in rec:
			print (x)

		domain = [('id','in',rec)]

		# view_id_tree = self.env['ir.ui.view'].search([('name','=',"semester.tree")])department_id=self.department_id.id)

		return {
		'type': 'ir.actions.act_window',
		 'name': ('Sale Orders'),
		 'res_model': 'sale.order',
		 'view_type': 'form',
		 'view_mode': 'tree,form',
		 # 'views': [(view_id_tree[0].id, 'tree'),(False,'form')],
		 'view_id ref=" sale.view_quotation_tree_with_onboarding"': '',
		 'target': 'current',
		 'domain': domain,

		}
	