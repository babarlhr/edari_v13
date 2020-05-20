# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class JobsExtension(models.Model):
	_inherit='hr.job'



	hiring_manager = fields.Many2one('hr.employee', string="Hiring Manager")
	job_type = fields.Many2one('job.type', string="Job Type")
	customer = fields.Many2one('res.partner', string="Customer")
	hiring_manager_client = fields.Many2one('res.partner', string="Hiring Manager Client")
	anticipated_start_date = fields.Date(string="Anticipated Start Date")
	budget = fields.Float(string="Budget")
	contract_length = fields.Float(string="Contract Length")
	estimated_gross_salary = fields.Float(string="Estimated Gross Salary")
	# so_count = fields.Integer(compute='_compute_so_count', string='Cost Card Count')
	visa_entity = fields.Many2one('visa.entity', string="Visa Entity")
	costcard_template = fields.Many2one('sale.order', string="Cost Card")
	working_days_type = fields.Char(string="Working Days Type")
	leave_type = fields.Char(string="Leave Type")

	work_days_type = fields.Selection([
		('twenty_two_days','22 Days'),
		('calender_days','Calender Days'),
		('actual_working_days','Actual Working Days'),
		('twenty_six_days','26 Days'),
		], string='Work Days Type', default="twenty_two_days", required = True)
	leave_type = fields.Selection([
		('one_day','One Day / Week'),
		('two_days','Two Days / Week'),
		], string='Leave Type', default="two_days")

	job_position_status = fields.Selection([
		('open','Open'),
		('closed','Closed'),
		], string='Job Position Status')
	# annual_leaves = fields.Float(string="Annual Leaves")
	# sick_leaves = fields.Float(string="Sick Leaves")
	template = fields.Many2one('costcard.template', string="Template")

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

	@api.onchange('customer')
	def get_domain(self):
		for x in self:
			id_list = []
			for index in x.customer.child_ids:
				id_list.append(index.id)
			return {'domain': {'hiring_manager_client':[('id','in',id_list)]}}


	@api.onchange('template')
	def get_work_leave_type(self):
		self.work_days_type = self.template.work_days_type
		self.leave_type = self.template.leave_type



	@api.onchange('name')
	def get_current_user(self):
		if not self.user_id:
			self.user_id = self.env.uid

	@api.onchange('customer')
	def template_domain(self):
		template_recs = self.env['costcard.template'].search([('job_position', '=', self.id),('customer','=',self.customer.id)])
		template_list = []
		for x in template_recs:
			template_list.append([x.id])
		self.domain_template = [(6, 0, template_list)]

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
	

	def create_so(self):
		# rec = self.env['sale.order'].search([('job_pos','=',self.id)]).ids
		# domain = [('id','=',rec)]
		if not self.costcard_template:
			so_rec = self.env['sale.order'].create({
				'job_pos':self.id,
				'template':self.template.id,
				'partner_id':self.customer.id,
				'no_of_months':self.contract_length,
				'work_days_type':self.work_days_type,
				'leave_type':self.leave_type,
				'per_month_gross_salary':self.estimated_gross_salary,
				'percentage':self.customer.default_edari_percentage,
				'costcard_type':'estimate',
				})
			self.costcard_template = so_rec.id
		else:
			print (self.customer.default_edari_percentage)
			print (type(self.customer.default_edari_percentage))
			if self.costcard_template.state == 'draft':
				self.costcard_template.job_pos = self.id
				self.costcard_template.template = self.template.id
				self.costcard_template.partner_id = self.customer.id
				self.costcard_template.no_of_months = self.contract_length
				self.costcard_template.work_days_type = self.work_days_type
				self.costcard_template.leave_type = self.leave_type
				self.costcard_template.per_month_gross_salary = self.estimated_gross_salary
				self.costcard_template.percentage = self.customer.default_edari_percentage
				self.costcard_template.costcard_type = 'estimate'
			else:
				raise ValidationError('Cost Card template is not in draft state.')
		self.costcard_template.get_order_lines()
		self.costcard_template.create_edari_fee()

		return {
		'type': 'ir.actions.act_window',
		 'name': ('Cost Card'),
		 'res_model': 'sale.order',
		 'view_type': 'form',
		 'view_mode': 'tree,form',
		 # 'context': {
		 # 'default_job_pos':self.id,
		 # 'default_template':self.template.id,
		 # 'default_partner_id':self.customer.id,
		 # 'default_no_of_months':self.contract_length,
		 # 'default_per_month_gross_salary':self.budget,
		 # 'default_costcard_type':'estimate',
		 # },
		 # 'view_id ref=" sale.view_quotation_tree_with_onboarding"': '',
		 'target': 'current',
		 'domain': [('id','=',self.costcard_template.id)],
		}

	def so_smart_button(self):

		recs = []
		recs.append(self.costcard_template.id)
		applications = self.env['hr.applicant'].search([('job_id','=',self.id)])
		for app in applications:
			recs.append(app.cost_card.id)
		rec = self.env['sale.order'].search(['|',('job_pos','=',self.id),('applicant','!=',False)]).ids

		domain = [('id','=',recs)]
		
		return {
		'type': 'ir.actions.act_window',
		 'name': ('Cost Cards'),
		 'res_model': 'sale.order',
		 'view_type': 'form',
		 'view_mode': 'tree,form',
		 
		 'target': 'current',
		 'domain': domain,
		 
		}

