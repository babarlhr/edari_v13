# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class HrEmployeeExtension(models.Model):
	_inherit = 'hr.employee'




	employee_code = fields.Char("Employee Code")
	cost_card = fields.Many2one("sale.order", "Cost Card")
	wage = fields.Float("Wage")


	@api.model
	def create(self, vals):
		new_record = super(HrEmployeeExtension, self).create(vals)
		# updating wage in employee
		for x in new_record.contract_ids:
			if x.state == 'open':
				x.wage = new_record.wage
		return new_record

	def write(self, vals):
		rec = super(HrEmployeeExtension, self).write(vals)
		# updating wage in employee
		if 'wage' in vals:
			for x in self.contract_ids:
				if x.state == 'open':
					x.wage = vals['wage']
		return rec
	def create_so(self):
		if not self.cost_card:
			so_rec = self.env['sale.order'].create({
				'candidate_name':self.name,
				# 'applicant':self.id,
				'employee':self.id,
				# 'contract':self.contract.id,
				# 'contract_start_date':self.availability,
				# 'per_month_gross_salary':self.salary_expected,
				'job_pos':self.job_id.id,
				'template':self.job_id.template.id,
				'partner_id':self.job_id.customer.id,
				'no_of_months':int(self.job_id.contract_length),
				})
			self.cost_card = so_rec.id
			# self.cost_card.get_order_lines()
		else:
			if self.cost_card.state == 'draft':
				self.candidate_name = self.name,
				# self.applicant = self.id,
				self.employee = self.id,
				# self.contract = self.contract.id,
				# self.contract_start_date = self.availability,
				# self.per_month_gross_salary = self.salary_expected,
				self.job_pos = self.job_id.id,
				self.template = self.job_id.template.id,
				self.partner_id = self.job_id.customer.id,
				self.no_of_months = int(self.job_id.contract_length),
				# self.cost_card.get_order_lines()
			else:
				raise Warning('Cost Card is not in quotation state.')



