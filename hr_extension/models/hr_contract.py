# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError
from dateutil.relativedelta import *


class HrContractExtension(models.Model):
	_inherit = 'hr.contract'

	customer = fields.Many2one()
	contract_length = fields.Char("Contract Length")
	cost_card = fields.Many2one('sale.order',"Cost Card")
	line_manager_client = fields.Many2one('res.partner')
	line_manager_domain = fields.Many2many('res.partner',compute = "_filtered_managers")




	@api.depends("customer")
	def _filtered_managers(self):
		id_list = []
		if self.customer:
			for index in self.customer.child_ids:
				id_list.append(index.id)
		
		self.line_manager_domain = [(6,0, id_list)]






	@api.model
	def create(self, vals):
		new_record = super(HrContractExtension, self).create(vals)
		new_record.AllocateLeaves()
		# updating wage in contract
		new_record.UpdateSo()
		new_record.UpdateLineManager()
		
		return new_record

	def write(self,vals):
		rec = super(HrContractExtension,self).write(vals)
		self.AllocateLeaves()
		self.UpdateSo()
		self.UpdateLineManager()
		return rec

	# @api.onchange('date_start')
	# def get_default_values(self):
		
	# 	if self.employee_id:
	# 		self.name = self.employee_id.name
			
			# if self.employee_id.cost_card:
			# 	if not self.cost_card:
					
			# 	if not self.wage:


	def UpdateLineManager(self):
		if not self.line_manager_client.parent_id:
			self.line_manager_client.parent_id = self.customer.id

	def UpdateSo(self):
		if self.cost_card:
			self.cost_card.state = "sale"
			self.cost_card.contract_start_date = self.date_start
			self.cost_card.contract_end_date = self.date_end
			self.cost_card.contract = self.id
			self.cost_card.costcard_type = "cost_card"
			self.cost_card.state = "done"
	@api.onchange('date_start')
	def GetDate(self):
		if self.date_start:
			self.name = self.employee_id.name
			self.cost_card = self.employee_id.cost_card.id
			self.contract_length = self.cost_card.no_of_months
			self.wage = self.cost_card.per_month_gross_salary
			self.date_end = self.date_start + relativedelta(months=int(self.cost_card.no_of_months))- relativedelta(days=1) 

	def AllocateLeaves(self):
		if self.state == 'open':
			if self.cost_card:
				sick_leave_accruing = False
				annual_leave_accruing = False		
				for x in self.cost_card.order_line:
					if x.product_id.name == "Sick Leave Cost" and x.price_unit > 0:
						sick_leave_accruing = True
					if x.product_id.name == "Annual Leave Cost" and x.price_unit > 0:
						annual_leave_accruing = True


				sick_leave_days = 0
				annual_leave_days = 0
				for x in self.cost_card.template.template_tree:
					if x.service_name.name == "Sick Leave Days":
						sick_leave_days = self.cost_card.CalculateLeaveDays(x)
					if x.service_name.name == "Annual Leave Days":
						annual_leave_days = self.cost_card.CalculateLeaveDays(x)


				if sick_leave_days:
					leave_type = self.env['hr.leave.type'].search([('name','=',"Sick Leave Days")])
					allocated_leaves = self.env['hr.leave.allocation'].search([('name','=',"Sick Leave Days"),('employee_id','=',self.employee_id.id),('state','=',"validate")])
					if not allocated_leaves:
						if sick_leave_accruing:
							self.CreateLeaveAllocations("Sick Leave Days",leave_type.id,None,"accrual",sick_leave_days/self.cost_card.no_of_months)
						else:
							self.CreateLeaveAllocations("Sick Leave Days",leave_type.id,sick_leave_days,"regular",1)

				if annual_leave_days:
					leave_type = self.env['hr.leave.type'].search([('name','=',"Annual Leave Days")])
					allocated_leaves = self.env['hr.leave.allocation'].search([('name','=',"Annual Leave Days"),('employee_id','=',self.employee_id.id),('state','=',"validate")])

					if not allocated_leaves:
						if annual_leave_accruing:
							self.CreateLeaveAllocations("Annual Leave Days",leave_type.id,None,"accrual",annual_leave_days/self.cost_card.no_of_months)
						else:
							self.CreateLeaveAllocations("Annual Leave Days",leave_type.id,annual_leave_days,"regular",1)




	def CreateLeaveAllocations(self,leave_name,leave_type,days,allocation_type,number_per_interval):
		create_allocation = self.env['hr.leave.allocation'].create({
			'name': leave_name,
			'employee_id':self.employee_id.id,
			'holiday_status_id':leave_type,
			'number_of_days_display':days,
			'number_of_days':days,
			'allocation_type':allocation_type,
			'number_per_interval':number_per_interval,
			'unit_per_interval':"days",
			'interval_number':1,
			'interval_unit':"months",

			})
		create_allocation.action_approve()
					
class HRPayslipExtension(models.Model):
	_inherit = 'hr.payslip.input'

	description = fields.Char(string = "Details")				
