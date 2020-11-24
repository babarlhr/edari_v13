# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError, UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import datetime as dt
import calendar
# import pandas as pd


class SaleOrderExt(models.Model):
	_inherit='sale.order'

	no_of_months = fields.Float(string="No of Months")
	sequence_number = fields.Char(string="Sequence No", copy = False)
	per_month_gross_salary = fields.Float(string="Per Month Gross Salary")
	template = fields.Many2one('costcard.template', string="Template")
	job_pos = fields.Many2one('hr.job', string="Job Position")
	version = fields.Char(string="Version No")
	first_approval = fields.Many2one('res.users',string = "First Approval", copy = False)
	second_approval = fields.Many2one('res.users',string = "Second Approval", copy = False)
	# interval = fields.Integer(string="Interval")
	contract_start_date = fields.Date(string="Contract Start Date")
	contract_end_date = fields.Date(string="Contract End Date")
	estimated_start_date = fields.Date(string="Estimated Start Date")
	date_invoice = fields.Date(string="Invoice Date")
	invoice_amount = fields.Float(string="Invoice Amount")
	percentage = fields.Float(string="Percentage %" ,digits=(4,4))
	invoice_id = fields.Many2one('account.move', string="Invoice")
	applicant = fields.Many2one('hr.applicant', string="Applicant")
	employee = fields.Many2one('hr.employee', string="Employee")
	contract = fields.Many2one('hr.contract', string="Contract" , copy=False)
	candidate_name = fields.Char(string="Candidate Name")
	customer_po_no = fields.Char(string="Customer PO Number")
	month_days_deduction = fields.Boolean(string="Month Days Deduction")
	monthly_deduction = fields.Boolean(string="Monthly Deduction")
	applicant_approve_check = fields.Boolean(string="Approved Applicant")
	budget = fields.Float(string="Budget", related="job_pos.budget")
	unlock_check = fields.Boolean(string="Un Lock Check")
	out_of_system_invoiced_amount = fields.Float(string="Out Of System Invoiced Amount")
	inv_attention = fields.Char("Invoice Attention")
	invoice_requester = fields.Many2one('res.partner',string="Invoice Requester")
	invoice_buyer = fields.Many2one('res.partner',string="Invoice Buyer")
	hiring_contact_client_dom = fields.Many2many('res.partner',compute = "GetContactDOM")
	extensions = fields.Char(
	    string='Extension No.',
	)
	order_line_2 = fields.One2many('sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=False, auto_join=True)
	percentage_2 = fields.Float(string="Percentage % (Mod)" ,digits=(4,4))
	per_month_gross_salary_2 = fields.Float(string="Per Month Gross Salary (Mod)")



	so_type = fields.Selection([
		('cost_card','Cost Card'),
		('sale_order','Sale Order'),
		], string='SO Type',default = 'cost_card')

	costcard_type = fields.Selection([
		('estimate','Estimate'),
		('cost_card','Cost Card'),
		], string='Cost Card Type',default="cost_card",required = True)
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
	contract_state = fields.Selection([
		('draft','New'),
		('open','Running'),
		('close','Expired'),
		('cancel','Cancelled'),
		], string='Contract State', default="draft")


	def FirstApproval(self):
		self.first_approval = self.env.uid
		if self.first_approval and self.second_approval:
			self.state = "done"
			self.applicant.approve_btn()

	def SecondApproval(self):
		self.second_approval = self.env.uid
		if self.first_approval and self.second_approval:
			self.state = "done"
			self.applicant.approve_btn()

	def ActionCancel(self):
		self.state = "draft"
		self.unlock_check = True
	
	def GetContactDOM(self):
		for x in self:
			id_list = []
			for index in x.partner_id.child_ids:
				id_list.append(index.id)

		self.hiring_contact_client_dom = [(6, 0, id_list)]


	@api.depends('order_line.invoice_lines')
	def _get_invoiced(self):
		# The invoice_ids are obtained thanks to the invoice lines of the SO
		# lines, and we also search for possible refunds created directly from
		# existing invoices. This is necessary since such a refund is not
		# directly linked to the SO.

		if self.so_type == "cost_card":

			for order in self:
				invoices = self.env['account.move'].search([('sale_order_id','=',order.id)])
				# invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.type in ('out_invoice', 'out_refund'))
				order.invoice_ids = invoices
				order.invoice_count = len(invoices)
		elif self.so_type == "sale_order":
			for order in self:
				invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.type in ('out_invoice', 'out_refund'))
				order.invoice_ids = invoices
				order.invoice_count = len(invoices)
		else:
			for order in self:
				order.invoice_count = 0



	def approve_applicant(self):
		if self.applicant:
			recs = self.env['hr.recruitment.stage'].search([('name','=','In Approvals')])
			self.applicant.stage_id = recs.id
			# self.applicant.approve_btn()
			self.applicant_approve_check = True


	def get_handle_sequence(self):
		if self.template:
			for lines in self.order_line:
				costcard_line_rec = self.env['costcard.template.tree'].search([('service_name','=',lines.product_id.id),('tree_link','=',self.template.id)])
				lines.handle = costcard_line_rec.handle

	def UpdateSOName(self):
		# cost_card_name = ""
		# if self.costcard_type == "estimate":
		# 	cost_card_name = "Estimate"
		# if self.costcard_type == "cost_card":
		# 	cost_card_name = "Cost Card"

		date=" "
		if self.contract.date_start:
			date=datetime.strftime(self.contract.date_start,'%d/%m/%Y')

		if self.partner_id.trading_as==False:
			client_name=self.partner_id.name[:3]
		else:
			client_name =self.partner_id.trading_as 
		
		applicant_name = ""
		if self.contract:
			applicant_name = self.contract.employee_id.name
		elif self.job_pos:
			applicant_name = self.job_pos.name
		else:
			applicant_name = self.partner_id.name
		if self.extensions == False:
			extensions = ""
		else:
			extensions = self.extensions
		if not self.sequence_number:
			self.sequence_number = self.name

		self.name = self.sequence_number + "-" +dict(self._fields['costcard_type'].selection).get(self.costcard_type)+"-"+client_name+"-"+applicant_name+"-"+date+"-"+extensions



	# @api.onchange('contract_start_date','no_of_months')
	# def get_contract_end_date(self):
	#   if self.contract_start_date and self.no_of_months:
	#       self.contract_end_date = self.contract_start_date + (relativedelta(months = self.no_of_months))
	#   else:
	#       self.contract_end_date = self.contract_start_date


	# def create_invoice(self):
	#   self.create_journal_entry()
	#   print ("Create Journal Entry")

	# new way of creating invoice START
	def prepare_invoice(self,date_invoice,month_invoice,from_date,to_date):
		journal = self.env['account.move'].with_context(force_company=self.company_id.id, default_type='out_invoice')._get_default_journal()
		if not journal:
			raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))
		# if self.contract and self.contract_state =='open':
		invoice_vals = {
			# 'ref': self.client_order_ref or '',
			'ref': self.name,
			'type': 'out_invoice',
			'narration': self.note,
			'currency_id': self.pricelist_id.currency_id.id,
			'campaign_id': self.campaign_id.id,
			'medium_id': self.medium_id.id,
			'automated_invoice': True,
			'source_id': self.source_id.id,
			'invoice_user_id': self.user_id and self.user_id.id,
			'team_id': self.team_id.id,
			'partner_id': self.partner_invoice_id.id,
			'employee': self.contract.employee_id.id,
			'partner_shipping_id': self.partner_shipping_id.id,
			'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
			'invoice_origin': self.name,
			'invoice_date':month_invoice,
			'invoice_month':date_invoice,
			'from_date':from_date,
			'to_date':to_date,
			'invoice_payment_term_id': self.payment_term_id.id,
			'invoice_payment_ref': self.reference,
			'invoice_requester': self.invoice_requester.id,
			'sale_order_id': self.id,
			'transaction_ids': [(6, 0, self.transaction_ids.ids)],
			'invoice_line_ids': [],
		}
		# else:
		#   raise ValidationError('Contract not available or not in Open state.')

		return invoice_vals


		# old method to create invoice
		# self.create_journal_entry()

	
	# Function to count do of days in a month
	def number_of_days_in_month(self, year, month):
		return monthrange(year, month)[1]

	def add_days_to_date(self, date):
		temp = str(date)
		days = int(temp[-2:])
		days += 1
		temp = temp[:-2]+str(days)

	def add_month_to_date(self, date):
		temp = str(date)
		month = int(temp[5:7])
		year = int(temp[0:4])
		day = int(temp[8:])
		if month == 12:
			day = 1
			month = 1
			year += 1
			temp = str(year)+"-0"+str(month)+"-0"+str(day)
		else:
			month += 1
			temp = temp[0:5]+str(month)+temp[7:]
		return temp

	def sub_days_to_date(self, date):
		temp = str(date)
		days = int(temp[-2:])
		days -= 1
		temp = temp[:-2]+str(days)

	def sub_month_to_date(self, date):
		temp = str(date)
		day = int(temp[8:])
		month = int(temp[5:7])
		year = int(temp[0:4])
		if month == 1:
			day = self.number_of_days_in_month(int(year), int(month))
			month = 12
			year -=1
			temp = str(year)+"-"+str(month)+"-"+str(day)
		else:
			month -= 1
			temp = temp[0:5]+str(month)+temp[7:]
		return temp

	############## Function to calculate leave balance total START ##############
	def calculate_leave_balance(self,date_invoice,leave_name):



		unique_holidays = []
		holiday_rec = self.env['custom.holiday.tree'].search([('tree_link.year','=',str(date_invoice.year))])
		for holiday_index in holiday_rec:
			if not holiday_index.day in unique_holidays:
				unique_holidays.append(holiday_index.date)

		employee_id = None
		if self.employee:
			employee_id = self.employee.id
		elif self.contract:
			employee_id = self.contract.employee_id.id
		leaves = self.env['hr.leave'].search([('employee_id','=',employee_id),('state','=','validate')])
		total_leaves = 0
		leave_name_days = 0
		leave_name_days = 0
		leave_days_list_specific = []
		leave_days_list = []
		for x in leaves:
			per_request_leaves = 0

			if date_invoice.replace(day=1) == x.request_date_from.replace(day=1) or date_invoice.replace(day=1) == x.request_date_to.replace(day=1):
				


				# getting list of days
				delta = x.request_date_to - x.request_date_from

				if delta.days == 0:
					delta_days = 1
				else:
					delta_days = delta.days
				for i in range(delta_days + 1):
					day = x.request_date_from + timedelta(days=i)
					if day.replace(day=1) == date_invoice.replace(day=1):
						if self.leave_type == "two_days":
							if day.weekday() != 4 and day.weekday() != 5:
								leave_days_list.append(day)
								if x.request_unit_half:
									total_leaves += 0.5
									if x.holiday_status_id.name == leave_name:
										leave_name_days += 0.5
										leave_days_list_specific.append(day)
								else:
									total_leaves += 1
									if x.holiday_status_id.name == leave_name:
										leave_name_days += 1
										leave_days_list_specific.append(day)
						if self.leave_type == "one_day":
							if day.weekday() != 4 :
								leave_days_list.append(day)
								if x.request_unit_half:
									total_leaves += 0.5
									if x.holiday_status_id.name == leave_name:
										leave_name_days += 0.5
										leave_days_list_specific.append(day)
								else:
									total_leaves += 1
									if x.holiday_status_id.name == leave_name:
										leave_name_days += 1
										leave_days_list_specific.append(day)


				for z in unique_holidays:
					if z in leave_days_list:
						leave_days_list.remove(z)
						
						total_leaves -= 1
					if z in leave_days_list_specific:
						leave_days_list_specific.remove(z)

						leave_name_days -= 1


		return [total_leaves,leave_name_days]


	def CalculateLeavesPayroll(self,date,leave_name):
		return self.calculate_leave_balance(date,leave_name)[1]



		
	############### Function to calculate leave balance total ENDS  #############

	############## Function to calculate Holidays total START ##############
	def calculate_holidays(self,interval_type,date_invoice):
		holidays = 0

		if interval_type == "start":
			holiday_rec = self.env['custom.holiday.tree'].search([('tree_link.year','=',str(date_invoice.year)),('date','>=',self.contract_start_date)])
		elif interval_type == "end":
			holiday_rec = self.env['custom.holiday.tree'].search([('tree_link.year','=',str(date_invoice.year)),('date','<=',self.contract_end_date)])
			print (holiday_rec)
		else:
			holiday_rec = self.env['custom.holiday.tree'].search([('tree_link.year','=',str(date_invoice.year))])
		for y in holiday_rec:
			if date_invoice.replace(day=1) == y.date.replace(day=1):
				if self.leave_type == "two_days":
					if y.date.weekday() !=4 and y.date.weekday() != 5 :

						holidays +=1
				if self.leave_type == "one_day":
					if y.date.weekday() !=4:
						holidays +=1
		return holidays
	############### Function to calculate Holidays total ENDS  #############


	################# Calculating salary according to days START #################
	def per_day_devisor(self,date_invoice):
		
		if self.work_days_type == 'twenty_two_days':
			return 22
		
		if self.work_days_type == 'twenty_six_days':
			return 26

		if self.work_days_type == "actual_working_days":
			total_days = self.number_of_days_in_month(date_invoice.year, date_invoice.month)
			weekends = self.calculate_weekends(date_invoice,"regular")
			# holidays = self.calculate_holidays()
			net_days = total_days - weekends


			return net_days

		if self.work_days_type == 'calender_days':
			
			return self.number_of_days_in_month(date_invoice.year, date_invoice.month)
		


	def calculate_working_days(self, contract_date, month_interval):
		working_days = 0
		relevant_date = contract_date
		
		last_day = calendar.monthrange(int(relevant_date.year),int(relevant_date.month))[1]
		last_date = relevant_date.replace(day=last_day)
		
		day = contract_date.replace(day=1)
		single_day = dt.timedelta(days=1)

		if month_interval == "start":
			start_date = relevant_date
			end_date = last_date
		if month_interval == "end":
			start_date = day
			end_date = relevant_date

		if self.work_days_type == 'twenty_two_days':
			while start_date <= end_date:
				if start_date.weekday() != 4 and start_date.weekday() != 5:
					if working_days < 22:
						working_days += 1
				start_date += single_day
		
		if self.work_days_type == 'calender_days':
			while start_date <= end_date:
				working_days += 1
				start_date += single_day

		if self.work_days_type == 'twenty_six_days':
			while start_date <= end_date:
				if start_date.weekday() != 4:
					if working_days < 26:
						working_days += 1
				start_date += single_day

		if self.work_days_type == 'actual_working_days':
			while start_date <= end_date:
				if self.leave_type == 'one_day':
					if start_date.weekday() != 4:
						working_days += 1
					start_date += single_day
				if self.leave_type == "two_days":
					if start_date.weekday() != 4 and start_date.weekday() != 5:
						working_days += 1
					start_date += single_day

		return working_days
	


	def calculate_weekends(self,contract_date, month_interval):

		relevant_date = contract_date
		
		last_day = calendar.monthrange(int(relevant_date.year),int(relevant_date.month))[1]
		last_date = relevant_date.replace(day=last_day)
		
		day = contract_date.replace(day=1)
		single_day = dt.timedelta(days=1)

		if month_interval == "start":
			start_date = relevant_date
			end_date = last_date
		if month_interval == "end":
			start_date = day
			end_date = relevant_date
		if month_interval == "regular":
			start_date = day
			end_date = last_date
		days_to_deduct = 0

		while start_date <= end_date:
			if self.leave_type == "two_days":
				if start_date.weekday() == 4 or start_date.weekday() == 5:
					days_to_deduct += 1
				start_date += single_day
			if self.leave_type == "one_day":
				if start_date.weekday() == 4:
					days_to_deduct += 1
				start_date += single_day

		return days_to_deduct
	################# Calculating salary according to days ENDS #################


	def recompute_func(self, line, code_dict,cumulative_total):
		costcard_template_rec = self.env['costcard.template.tree'].search([('service_name','=',line.product_id.id),('tree_link','=',self.template.id),('code','=',line.code)])


		global compute_result
		global compute_qty
		
		compute_result = 0
		compute_qty = 0

		salary = self.per_month_gross_salary
		no_months = self.no_of_months
		edari_service_percent = self.percentage
		salary_2 = self.per_month_gross_salary_2
		edari_service_percent_2 = self.percentage_2
		# cumulative_total = 0
		edari_fee = 0

		if costcard_template_rec.computation_formula:
			expression = 'global compute_result;\n'+costcard_template_rec.computation_formula
		else:
			expression = 'global compute_result;\n'

		try:
			exec(expression)
			code_dict[line.code] = compute_result

			globals().update(code_dict)
		except Exception as e:
			raise ValidationError('Error..!\n'+str(e))

		return compute_result

	def FinalWorkingDays(self,date_invoice,starting_month,ending_month):
		t_date = date_invoice

		# divisor and working_days variable are used for finding invoice line amount
		divisor = self.per_day_devisor(date_invoice)
		working_days = divisor
		month_interval = "regular"
		if starting_month == True:
			t_date = self.contract_start_date
			# divisor = self.per_day_devisor(t_date)
			month_interval = "start"
			working_days = self.calculate_working_days(t_date, month_interval)
		if ending_month == True:
			month_interval = "end"
			t_date = self.contract_end_date
			# divisor = self.per_day_devisor(t_date)
			working_days = self.calculate_working_days(t_date, month_interval)

		no_of_holidays = 0
		no_of_holidays_wd = 0
		if self.work_days_type == "actual_working_days":
			no_of_holidays = self.calculate_holidays("Regular",date_invoice)
			no_of_holidays_wd = self.calculate_holidays(month_interval,date_invoice)
			divisor -= no_of_holidays

		working_days -= (self.calculate_leave_balance(date_invoice,None)[0] + no_of_holidays_wd)

		return [working_days,divisor]



	def create_invoice(self,date_invoice,month_invoice):
		if not self.contract_start_date:
			raise ValidationError("Please input Contract Start Date")
		if not self.contract_end_date:
			raise ValidationError("Please input Contract End Date")
		# for line in self.order_line:

		#####################################################################################
		edari_product = self.env['product.product'].search([('name','=','Edari Service Fee')],limit=1)

		# Untaxed amounts
		print ("Check1")
		move_lines_list = []
		credit_sum = 0
		starting_month = False
		ending_month = False
		lines_not_to_add = []
		if date_invoice.month == self.contract_start_date.month and date_invoice.year == self.contract_start_date.year:
			lines_not_to_add = ['end']
			starting_month = True
			invoice_date_from = self.contract_start_date
			invoice_date_to = monthrange(date_invoice.year,date_invoice.month)[1]
			invoice_date_to_date = dt.date(date_invoice.year, date_invoice.month, invoice_date_to)


		elif date_invoice.month == self.contract_end_date.month and date_invoice.year == self.contract_end_date.year:
			lines_not_to_add = ['upfront']
			ending_month = True
			invoice_date_from = self.contract_end_date.replace(day=1)
			invoice_date_to_date = self.contract_end_date

		else:
			lines_not_to_add = ['end','upfront']
			invoice_date_from = dt.date(date_invoice.year, date_invoice.month, 1)
			invoice_date_to = monthrange(date_invoice.year,date_invoice.month)[1]
			invoice_date_to_date = dt.date(date_invoice.year, date_invoice.month, invoice_date_to)

		invoice_vals_list = []
		invoice_vals = self.prepare_invoice(date_invoice,month_invoice,invoice_date_from,invoice_date_to_date)

		
		values = self.FinalWorkingDays(date_invoice,starting_month,ending_month)
		working_days = values[0]
		divisor = values[1]

		print (values)


		code_dict_new = {}
		total_invoice_amount = 0
		for line in self.order_line:
			if line.price_unit != 0:
				amount = 0
				
				if not line.payment_type in lines_not_to_add:
					print (line.code)


					# qty in months check
					if line.as_of_date:
						line_start_date = line.as_of_date.replace(day=1)
						line_end_date = line_start_date+(relativedelta(months = (int(line.product_uom_qty)), days=-1))
					else:
						line_end_date = self.contract_start_date+(relativedelta(months = (int(line.product_uom_qty)), days=-1))
						line_start_date = self.contract_start_date

					if (date_invoice.replace(day=1) <= line_end_date.replace(day=1)) and (date_invoice.replace(day=1) >= line_start_date.replace(day=1)):
					
						if line.payment_type == 'interval':
							amount = line.price_unit
							total_invoice_amount += line.price_unit
						else:
							amount = line.price_subtotal
							total_invoice_amount += line.price_subtotal


						if line.based_on_wd:
							per_day = amount/divisor
							print (per_day)
							amount = per_day*working_days

						# Calculate leave balance
						balance = amount
						recompute_result = 0
						code_dict_new[line.code] = balance
						globals().update(code_dict_new)
						if line.recomputable:
							cumulative_total = 0
							for rec in self.order_line:
								if rec.code == line.code:
									break
								cumulative_total += code_dict_new[rec.code]


							recompute_result = self.recompute_func(line, code_dict_new,cumulative_total)							
							balance = recompute_result
						
						invoice_vals['invoice_line_ids'].append(line.prepare_invoice_line(balance,line.product_id.name,line.product_id.id))
						credit_sum += balance
					else:
						balance = 0
						code_dict_new[line.code] = balance
						globals().update(code_dict_new)

				
				# setting those variables which are not falling in date limit as zero
				else:
					print (line.code)
					balance = 0
					code_dict_new[line.code] = balance
					globals().update(code_dict_new)
			else:
				balance = 0
				code_dict_new[line.code] = balance
				globals().update(code_dict_new)

		
		if not invoice_vals['invoice_line_ids']:
			raise UserError('There is no invoiceable line. Please check the contract length compared to the number of months specified in the cost card.')

		remaining_amount = 0
		if ending_month == True:

			all_invoices_amount = 0
			if self.out_of_system_invoiced_amount:
				all_invoices_amount += self.out_of_system_invoiced_amount
			all_invoices = self.env['account.move'].search([('sale_order_id','=',self.id)])
			for inv in all_invoices:
				all_invoices_amount += inv.amount_untaxed
			remaining_amount = self.amount_untaxed -(all_invoices_amount + credit_sum) 
			if remaining_amount != 0:


				invoice_vals['invoice_line_ids'].append(line.prepare_invoice_line(remaining_amount,"Final Invoice Adjustment",None))

		invoice_vals_list.append(invoice_vals)

		total_invoice_amount += remaining_amount 


		# 3) Create invoices.
		moves = self.env['account.move'].with_context(default_type='out_invoice').create(invoice_vals_list)

		moves.pro_rate_adjust = total_invoice_amount - moves.amount_untaxed
		moves.leave_taken = self.CalculateLeavesPayroll(date_invoice,"Annual Leave Days")
		moves.sick_days_taken = self.CalculateLeavesPayroll(date_invoice,"Sick Leave Days")



		########### update accrual entries ##################

		for acc in self.order_line:
			if acc.product_id.accruing_account_id:
				if acc.product_id.property_account_expense_id:
					debit_account = acc.product_id.property_account_income_id.id
				else:
					debit_account = acc.product_id.categ_id.property_account_income_categ_id.id
				for mv in moves.line_ids:
					if mv.name == acc.product_id.name:
						line_amount = mv.credit
						break

				if line_amount > 0:


					moves.write({
						'line_ids': [
								(0, 0, {
									'account_id':debit_account,
									'name':"Accrued Adjustment",
									'debit':line_amount,
									'credit':0,
									'partner_id':self.partner_id.id,
								}),
					
								(0, 0, {
									'account_id':acc.product_id.accruing_account_id.id,
									'name':"Accrued Adjustment",
									'debit':0,
									'credit':line_amount,
									'partner_id':self.contract.employee_id.partner_id.id,

									
								}),
							],
						}) 


		# Update journal items to merge individual lines
		merged = {}
		for mv in moves.line_ids:
			if mv.account_id.id not in merged:
				name = mv.name
				if mv.account_id.internal_group == 'income':
					name = "{} - {}".format(self.name, self.invoice_month)
				merged[mv.account_id.id] = {
					'account_id':mv.account_id.id,
					'name': name,
					'debit':0,
					'credit':0,
					'partner_id':self.partner_id.id,
				}
			
			merged[mv.account_id.id]['debit'] += mv.debit
			merged[mv.account_id.id]['credit'] += mv.credit

		## Fix debit / credit to keep 1 of the values and insert
		for mrg in merged:
			if mrg.debit > mrg.credit:
				mrg.debit = mrg.debit - mrg.credit
				mrg.credit = 0
			else:
				mrg.credit = mrg.credit - mrg.debit
				mrg.debit = 0
			
			moves.write({
				'line_ids': [
					(0,0, mrg)
				]
			})
		

		return moves




	def CalculateLeaveDays(self,record_id):
		salary = self.per_month_gross_salary
		no_months = self.no_of_months
		edari_service_percent = self.percentage
		salary_2 = self.per_month_gross_salary_2
		edari_service_percent_2 = self.percentage_2
		cumulative_total = 0
		edari_fee = 0


		global compute_result

		if record_id.computation_formula:
			expression = 'global compute_result;\n'+record_id.computation_formula
		else:
			expression = 'global compute_result;\n'

		try:
			exec(expression)
		
		except Exception as e:
			raise ValidationError('Error..!\n'+str(e))

		return compute_result

	# @api.onchange('template')
	def get_order_lines(self):

		edits = {}

		# computed_dict = {}
		for x in self.order_line:
			if not x.costcard_type == 'manual':
				edits[x.code] = {
					'as_of_date': x.as_of_date,
					'product_uom_qty': x.product_uom_qty
				}
			#   if x.product_uom_qty > 1:
			#       computed_dict[x.product_id.id] = x.product_uom_qty
				x.unlink()

		if self.template:

			code_dict = {}

			salary = self.per_month_gross_salary
			no_months = self.no_of_months
			edari_service_percent = self.percentage
			salary_2 = self.per_month_gross_salary_2
			edari_service_percent_2 = self.percentage_2
			cumulative_total = 0
			edari_fee = 0

			


			template_tree_recs = self.env['costcard.template.tree'].search([('tree_link','=',self.template.id)], order='handle')
			# for x in self.template.template_tree:
			for x in template_tree_recs:
				cumulative_check = True
				manual_amount_cumulative = 0
				for lines in self.order_line:
					if x.code == lines.code:
						if lines.costcard_type == "manual":
							cumulative_check = False
							manual_amount_cumulative = lines.price_unit
				if x.costcard_type == "calculation":
					cumulative_check = False

				# manual_amount_cumulative = 0
				# if x.costcard_type == "manual":
				# 	for lines in self.order_line:
				# 		if x.code == lines.code:
				# 			manual_amount_cumulative = lines.price_unit


				global compute_result
				global compute_qty
				
				compute_result = 0
				compute_qty = 0
				# if ' ' in x.computation_formula:
				# result = eval(x.computation_formula)
				if x.computation_formula:
					expression = 'global compute_result;\n'+x.computation_formula
				else:
					expression = 'global compute_result;\n'

				# Calculating qty
				if x.computation_qty:
					# print (compute_qty)
					qty_expression = 'global compute_qty;\n'+x.computation_qty
				else:
					qty_expression = 'global compute_qty;\n'
				# expression = x.computation_formula
				# expression.replace("result", "cost_card_compute_x1")
				# exec(x.computation_formula)
				
				try:
					exec(expression)
					exec(qty_expression)
					


				except Exception as e:
					raise ValidationError('Error..!\n'+str(e))

				# print (compute_result)
				

				qty = 0
				# if x.costcard_type in ['fixed','calculation']:
				# if x.costcard_type in ['manual']:
				# 	qty = 1


				
				# if x.costcard_type:
				# if x.costcard_type == 'manual':
				# else:
				#   # Changed to get date from compute date field
				qty = self.no_of_months

				saved_qty = 0
				try:
					if edits[x.code] and edits[x.code]['product_uom_qty']>0:
						# This is a regenerate over existing rows
						saved_qty = edits[x.code]['product_uom_qty']
						qty = saved_qty
				except:
					# ignore missing key
					saved_qty = 0
					
					# compute_result = 0
				if x.payment_type in ['upfront','end'] and x.costcard_type != 'manual':
					qty = 1

				if x.computation_qty:
					if saved_qty == 0:
						# if user edited quantities, keep what they got
						qty = compute_qty
					if compute_result and self.no_of_months and qty > 0:
						compute_result = compute_result * (self.no_of_months / qty)

				if cumulative_check == True:
					cumulative_total += compute_result 

				cumulative_total += manual_amount_cumulative


				# order_lines_list.append({
				manual_check = True
				for index in self.order_line:
					if index.product_id.id == x.service_name.id:
						manual_check = False
						index.get_manual_price_unit()
						code_dict[x.code] = index.price_unit
				
				if manual_check:
					# if x.service_name.id in computed_dict:
					#   qty = computed_dict[x.service_name.id]

					as_of = False
					try:
						as_of = edits[x.code]['as_of_date']
					except:
						# Key not defined
						as_of = False

					self.order_line.create({
						'product_id':x.service_name.id,
						# 'sale_order_template_id':self.id,
						'order_id':self.id,
						# 'product_uom_qty':self.no_of_months,
						'product_uom_qty':qty,
						# 'product_uom_qty':compute_qty,
						'price_unit':compute_result,
						'based_on_wd':x.based_on_wd,
						'payment_type':x.payment_type,
						'code':x.code,
						'recomputable':x.recomputable,
						'handle':x.handle,
						'categ_id':x.service_name.categ_id.id,
						'name':x.code or "",
						'costcard_type':x.costcard_type,
						'chargable':x.chargable,
						'as_of_date': as_of,
						})
					code_dict[x.code] = compute_result


					


				globals().update(code_dict)
				del compute_result
				del compute_qty

			# deleting global variables


			for x in code_dict.keys():
				del x

			for x in self.order_line:
				if x.costcard_type == 'calculation':
					x.unlink()

		else:
			self.order_line = None


	def CreateActivities(self):
		users = []
		first_approval = self.env.ref('so_extension.first_approval_cost_card_group')
		second_approval = self.env.ref('so_extension.second_approval_cost_card_group')
		for fir in first_approval.users:
			if fir.id not in [1,2]:
				users.append(fir.id)
		for sec in second_approval.users:
			if sec.id not in [1,2]:
				if sec.id not in users:
					users.append(sec.id)

		for us in users:
			self.env['mail.activity'].create({
					'res_id': self.id,
					'res_model_id': self.env['ir.model']._get('sale.order').id,
					'activity_type_id': self.env.ref('so_extension.activity_type').id,
					'summary': "Cost Card Number-" +self.name + " Needs your approval",
					'note': "Cost Card Number-" +self.name + " Needs your approval",
					'user_id': us,
				})

	def action_confirm(self):
		res = super(SaleOrderExt, self).action_confirm()
		if self.so_type == "cost_card":
			if not self.first_approval and not self.second_approval:
				self.CreateActivities()
			if self.first_approval and self.second_approval:
				self.state = "done"
		return res

	def create_edari_fee(self):
		return True


	@api.model
	def create(self, vals):
		new_record = super(SaleOrderExt, self).create(vals)

		if new_record.so_type == 'cost_card':
			self.UpdateLeaveType()

			if new_record.job_pos:
				print (new_record.job_pos.name)
				records = self.env['sale.order'].search([('job_pos','=',new_record.job_pos.id),('state','not in',['cancel','done'])])
				rec_len = len(records)
				if records:
					new_record.version = "V"+str(rec_len)
					print (new_record.version)
				else:
					new_record.version = "V1"
					print (new_record.version)
			new_record.get_handle_sequence()

			# new_record.get_contract_end_date()
			new_record.get_order_lines()

			# updating wage in employee
			if new_record.employee:
				new_record.employee.wage = new_record.per_month_gross_salary
		return new_record

	def write(self, vals):
		before=self.write_date

		rec = super(SaleOrderExt, self).write(vals)


		if 'per_month_gross_salary' in vals:
			self.applicant.salary_expected = vals['per_month_gross_salary']

			# updating wage in employee
			if self.employee:
				self.employee.wage = vals['per_month_gross_salary']

		after = self.write_date
		if before != after:
			if self.so_type == 'cost_card':
				if 'no_of_months' in vals or 'template' in vals or 'per_month_gross_salary' in vals or 'percentage' in vals or 'order_line' in vals or 'work_days_type' in vals  or 'per_month_gross_salary_2' in vals or 'percentage_2' in vals:
					self.get_order_lines()
					if 'template' in vals or 'order_line' in vals:
						self.get_handle_sequence()

		if 'name' not in vals:
			if self.so_type == 'cost_card':
				self.UpdateSOName()

		if 'work_days_type' in vals:
			self.UpdateLeaveType()

		return rec

	def UpdateLeaveType(self):
		if self.work_days_type == "twenty_two_days":
			self.leave_type = "two_days"
		if self.work_days_type == "twenty_six_days":
			self.leave_type = "one_day"

	def GetDivisorPayroll(self,date_from):
		no_of_holidays = 0
		days = 0
		days = self.per_day_devisor(date_from)
		no_of_holidays = self.calculate_holidays("Regular",date_from)
		return days - no_of_holidays

	def GetWorkingDaysPayroll(self,date_from,date_to):
		result = 0
		starting_month = False
		ending_month = False
		if date_from <= self.contract_start_date  <= date_to:
			starting_month = True
		if date_from <= self.contract_end_date  <= date_to:
			ending_month = True


		values = self.FinalWorkingDays(date_from,starting_month,ending_month)
		return values[0]

	@api.onchange('no_of_months')
	def UpdateManualMonths(self):
		for lines in self.order_line:
			if lines.costcard_type == "manual":
				lines.product_uom_qty = self.no_of_months
				lines.get_manual_price_unit()




class SOLineExt(models.Model):
	_inherit='sale.order.line'
	_order = 'handle'

	code = fields.Char(string="Code")
	handle = fields.Char(string="Handle", readonly=True, copy=False)
	chargable = fields.Boolean(string="Chargable")
	manual_amount = fields.Float(string="Manual Amount")
	categ_id = fields.Many2one('product.category', string="Product Category")
	based_on_wd = fields.Boolean(string="Based on WD")
	recomputable = fields.Boolean(string="Recomputable")
	offset = fields.Float(string="Offset")
	as_of_date = fields.Date(string="As Of Month")

	def _check_line_unlink(self):
		return False
		"""
		Check wether a line can be deleted or not.

		Lines cannot be deleted if the order is confirmed; downpayment
		lines who have not yet been invoiced bypass that exception.
		:rtype: recordset sale.order.line
		:returns: set of lines that cannot be deleted
		"""
		# return self.filtered(lambda line: line.state in ('sale', 'done') and (line.invoice_lines or not line.is_downpayment))





	def prepare_invoice_line(self,amount,name,product_id):
		"""
		Prepare the dict of values to create the new invoice line for a sales order line.
		:param qty: float quantity to invoice
		"""
		self.ensure_one()

		return {
			'display_type': self.display_type,
			'sequence': self.sequence,
			'name': name,
			'product_id': product_id,
			'product_uom_id': self.product_uom.id,
			'quantity': 1,
			'discount': self.discount,
			# 'price_unit': self.price_unit,
			'price_unit': amount,
			'tax_ids': [(6, 0, self.tax_id.ids)],
			'analytic_account_id': self.order_id.analytic_account_id.id,
			'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
			'sale_line_ids': [(4, self.id)],
		}

	@api.onchange('manual_amount','product_uom_qty')
	def get_manual_price_unit(self):
		if self.costcard_type == 'manual' and self.order_id.no_of_months>0:
			if not self.product_uom_qty:
				self.product_uom_qty = self.order_id.no_of_months
			self.price_unit = self.manual_amount/self.product_uom_qty

	@api.onchange('product_uom_qty')
	def get_price_unit_on_uom_change(self):
		if self.costcard_type == 'manual' and self.order_id.no_of_months>0:
			self.price_unit = self.manual_amount/self.product_uom_qty


	@api.onchange('product_uom')
	def product_uom_change(self):
		if not self.product_uom or not self.product_id:
			self.price_unit = 0.0
			return
		if self.order_id.pricelist_id and self.order_id.partner_id:
			product = self.product_id.with_context(
				lang=self.order_id.partner_id.lang,
				partner=self.order_id.partner_id,
				quantity=self.product_uom_qty,
				date=self.order_id.date_order,
				pricelist=self.order_id.pricelist_id.id,
				uom=self.product_uom.id,
				fiscal_position=self.env.context.get('fiscal_position')
			)
			self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)




	payment_type = fields.Selection([
		('upfront','Upfront'),
		('end','End'),
		('interval','Interval')
		], string='Payment Type')

	costcard_type = fields.Selection([
		('fixed','Fixed'),
		('manual','Manual'),
		('calculation','Calculation'),
		], string='Type')

