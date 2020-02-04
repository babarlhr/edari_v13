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
	# so_count = fields.Integer(compute='_compute_so_count', string='Cost Card Count')
	visa_entity = fields.Many2one('visa.entity', string="Visa Entity")
	costcard_template = fields.Many2one('sale.order', string="Cost Card")
	annual_leaves = fields.Float(string="Annual Leaves")
	sick_leaves = fields.Float(string="Sick Leaves")
	template = fields.Many2one('costcard.template', string="Template")
	domain_template = fields.Many2many('costcard.template', string="Domain Template")

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

	# @api.onchange('customer')
	# def template_domain(self):
	# 	print ("0000000000000000000000000")
	# 	template_recs = self.env['costcard.template'].search([('job_position', '=', self.id),('customer','=',self.customer.id)])
	# 	template_list = []
	# 	for x in template_recs:
	# 		template_list.append([x.id])
	# 	self.domain_template = [(6, 0, template_list)]

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
	

	# def so_smart_button(self):
	# 	rec = self.env['sale.order'].search([('job_pos','=',self.id)]).ids
	# 	domain = [('id','in',rec)]
	# 	return {
	# 	'type': 'ir.actions.act_window',
	# 	 'name': ('Sale Orders'),
	# 	 'res_model': 'sale.order',
	# 	 'view_type': 'form',
	# 	 'view_mode': 'tree,form',
	# 	 'context': {
	# 	 'default_job_pos':self.id,
	# 	 'default_template':self.template.id,
	# 	 'default_partner_id':self.customer.id,
	# 	 'default_no_of_months':self.contract_length,
	# 	 'default_per_month_gross_salary':self.budget,
	# 	 'default_costcard_type':'estimate',
	# 	 },
	# 	 'view_id ref=" sale.view_quotation_tree_with_onboarding"': '',
	# 	 'target': 'current',
	# 	 'domain': domain,
	# 	}


	def create_so(self):
		if not self.costcard_template:
			so_rec = self.env['sale.order'].create({
				'job_pos':self.id,
				'template':self.template.id,
				'partner_id':self.customer.id,
				'no_of_months':self.contract_length,
				'per_month_gross_salary':self.budget,
				'costcard_type':'estimate',
				})
			self.costcard_template = so_rec.id
		else:
			if self.costcard_template.state == 'draft':
				self.costcard_template.job_pos = self.id
				self.costcard_template.template = self.template.id
				self.costcard_template.partner_id = self.customer.id
				self.costcard_template.no_of_months = self.contract_length
				self.costcard_template.per_month_gross_salary = self.budget
				self.costcard_template.costcard_type = 'estimate'
			else:
				raise ValidationError('Cost Card template is not in draft state.')
