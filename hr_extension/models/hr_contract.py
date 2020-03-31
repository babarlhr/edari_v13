# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError
from dateutil.relativedelta import *


class HrContractExtension(models.Model):
	_inherit = 'hr.contract'

	contract_length = fields.Char("Contract Length")
	cost_card = fields.Many2one('sale.order',"Cost Card")

	# @api.depends('employee_id.cost_card')
	# def get_wage(self):
	# 	for x in self:
	# 		if x.employee_id:
	# 			if x.employee_id.cost_card:
	# 				x.wage = x.employee_id.cost_card.per_month_gross_salary


	def write(self,vals):
		rec = super(HrContractExtension,self).write(vals)
		if 'state' in vals and vals['state'] == 'open':
			so_rec = self.env['sale.order'].search([('id','=',self.cost_card.id)])
			if so_rec:
				so_rec.write({
					'contract_start_date':self.date_start,
					'contract_end_date':self.date_end,
					'contract_state':self.state,
						})
		return rec



	@api.model
	def create(self, vals):
		new_record = super(HrContractExtension, self).create(vals)
		# updating wage in contract
		if new_record.cost_card:
			new_record.cost_card.contract = new_record.id
		
		return new_record

	@api.onchange('employee_id','date_start')
	def get_default_values(self):
		
		if self.employee_id:
			self.name = self.employee_id.name
			self.cost_card = self.employee_id.cost_card.id
			self.contract_length = self.cost_card.no_of_months
			self.wage = self.cost_card.per_month_gross_salary
			self.date_end = self.date_start + relativedelta(months=+self.cost_card.no_of_months)
			# if self.employee_id.cost_card:
			# 	if not self.cost_card:
					
			# 	if not self.wage:
					
				

	

		




		