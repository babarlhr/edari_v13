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
		self.UpdateSo()
		return rec



	@api.model
	def create(self, vals):
		new_record = super(HrContractExtension, self).create(vals)
		# updating wage in contract
		new_record.UpdateSo()
		
		return new_record

	# @api.onchange('date_start')
	# def get_default_values(self):
		
	# 	if self.employee_id:
	# 		self.name = self.employee_id.name
			
			# if self.employee_id.cost_card:
			# 	if not self.cost_card:
					
			# 	if not self.wage:


	def UpdateSo(self):
		if self.cost_card:
			self.cost_card.state = "sale"
			self.cost_card.contract_start_date = self.date_start
			self.cost_card.contract_end_date = self.date_end
			self.cost_card.contract = self.id
			self.cost_card.state = "done"
	@api.onchange('date_start')
	def GetDate(self):
		if self.date_start:
			self.name = self.employee_id.name
			self.cost_card = self.employee_id.cost_card.id
			self.contract_length = self.cost_card.no_of_months
			self.wage = self.cost_card.per_month_gross_salary
			self.date_end = self.date_start + relativedelta(months=int(self.cost_card.no_of_months))- relativedelta(days=1) 
					
				

	

		




		