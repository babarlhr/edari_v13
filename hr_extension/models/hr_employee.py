# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class HrEmployeeExtension(models.Model):
	_inherit = 'hr.employee'




	employee_code = fields.Char("Employee Code")
	cost_card = fields.Many2one("sale.order", "Cost Card")
	customer = fields.Many2one('res.partner' , 'Customer')
	partner_id =fields.Many2one('res.partner',"Partner ID")
	wage = fields.Float("Wage")

	employee_type = fields.Selection([
		('edari_employee','Edari Employee'),
		('client_employee','Client Employee'),
		], string='Employee Type')


	@api.model
	def create(self, vals):
		
		new_record = super(HrEmployeeExtension, self).create(vals)
		# updating wage in employee
		new_record.AllocateLeaves()
		for x in new_record.contract_ids:
			if x.state == 'open':
				x.wage = new_record.wage
		partner_id = self.env['res.partner'].create([{'name': new_record.name,
										'phone':new_record.work_phone,
										'email':new_record.work_email,
										'mobile':new_record.mobile_phone,
										'is_employee':True}])
		new_record.partner_id = partner_id.id
		return new_record

	@api.onchange('name')
	def namechange(self):
		self.partner_id.write({'name':self.name})

	def write(self, vals):
		rec = super(HrEmployeeExtension, self).write(vals)
		# updating wage in employee
		self.AllocateLeaves()
		if 'wage' in vals:
			for x in self.contract_ids:
				if x.state == 'open':
					x.wage = vals['wage']
		
		if self.active == True:
			# record.active =False
			self.partner_id.write({'active':True})
		if self.active == False:
			self.partner_id.write({'active':False})			

		return rec


	def AllocateLeaves(self):

		if self.cost_card:
			for x in self.cost_card.template.template_tree:
				if x.service_name.name == "Sick Leave Days":
					leave_type = self.env['hr.leave.type'].search([('name','=',"Sick Leave Days")])
					days = self.cost_card.CalculateLeaveDays(x)
					print (days)
					allocated_leaves = self.env['hr.leave.allocation'].search([('name','=',"Sick Leave Days"),('employee_id','=',self.id)])
					if not allocated_leaves:
						self.CreateLeaveAllocations("Sick Leave Days",leave_type.id,int(days))
						# create_allocation.action_approve() 
				if x.service_name.name == "Annual Leave Days":
					leave_type = self.env['hr.leave.type'].search([('name','=',"Annual Leave Days")])
					days = self.cost_card.CalculateLeaveDays(x)
					print (days)
					allocated_leaves = self.env['hr.leave.allocation'].search([('name','=',"Annual Leave Days"),('employee_id','=',self.id)])
					if not allocated_leaves:
						self.CreateLeaveAllocations("Annual Leave Days",leave_type.id,int(days))
						# create_allocation.action_approve()


	def CreateLeaveAllocations(self,leave_name,leave_type,days):
		create_allocation = self.env['hr.leave.allocation'].create({
			'name': leave_name,
			'employee_id':self.id,
			'holiday_status_id':leave_type,
			'number_of_days_display':days,
			'number_of_days':days

			})
		create_allocation.action_approve()

# class res_partner_customized(models.Model):

# 	_inherit = 'res.partner'
# 	is_employee = fields.Boolean("Employee")


