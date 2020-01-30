# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class JobsExtension(models.Model):
	_inherit='hr.job'

	hiring_manager = fields.Many2one('hr.employee', string="Hiring Manager")
	job_type = fields.Many2one('job.type', string="Job Type")
	customer = fields.Many2one('res.partner')
	anticipated_start_date = fields.Date(string="Anticipated Start Date")
	budget = fields.Float(string="Budget")
	contract_length = fields.Float(string="Contract Length")
	template = fields.Many2one('costcard.template', string="Template")
	# so_count = fields.Integer(compute='_compute_so_count', string='Cost Card Count')
	visa_entity = fields.Many2one('visa.entity', string="Visa Entity")
	annual_leaves = fields.Float(string="Annual Leaves")
	sick_leaves = fields.Float(string="Sick Leaves")

	probation_period = fields.Selection([
		('three','3 months'),
		('six','6 months'),
		], string='Probation Period', default='three')
	notice_period = fields.Selection([
		('one','1 months'),
		('three','3 months'),
		], string='Notice Period', default='one')
	working_days = fields.Selection([
		('five','5 days'),
		('six','6 days'),
		], string='Working Days', default='five')


	# def _compute_so_count(self):
	# 	# so_data = self.env['sale.order'].sudo().read_group([('job_pos','in',self.ids)],['job_pos'],['job_pos'])
	# 	# result = dict((data['job_pos'][0], data['so_id_count']) for data in so_data)
	# 	for jobs in self:
	# 		print ("XXXXXXXXXXXXXXXXXXXXXXXXX")
	# 		print ("XXXXXXXXXXXXXXXXXXXXXXXXX")
	# 		print (jobs.id)
	# 		recs = self.env['sale.order'].search(['job_pos','=',jobs.id])
	# 		print (recs)
	# 		print (count)
	# 		print (type(count))
	# 		print ("XXXXXXXXXXXXXXXXXXXXXXXXX")
	# 		print ("XXXXXXXXXXXXXXXXXXXXXXXXX")
	# 		jobs.so_count = int(count)
	

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
		 'context': {
		 'default_job_pos':self.id,
		 'default_template':self.template.id,
		 'default_partner_id':self.customer.id,
		 'default_no_of_months':self.contract_length,
		 'default_per_month_gross_salary':self.budget,
		 },
		 'view_id ref=" sale.view_quotation_tree_with_onboarding"': '',
		 'target': 'current',
		 'domain': domain,

		}
	