# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError, UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SaleOrderExt(models.Model):
	_inherit='sale.order'

	no_of_months = fields.Integer(string="No of Months")
	per_month_gross_salary = fields.Float(string="Per Month Gross Salary")
	template = fields.Many2one('costcard.template', string="Template")
	job_pos = fields.Many2one('hr.job', string="Job Position")
	version = fields.Char(string="Version No")
	# interval = fields.Integer(string="Interval")
	contract_start_date = fields.Date(string="Contract Start Date")
	contract_end_date = fields.Date(string="Contract End Date")
	date_invoice = fields.Date(string="Invoice Date")
	invoice_amount = fields.Float(string="Invoice Amount")
	percentage = fields.Float(string="Percentage %")
	invoice_id = fields.Many2one('account.move', string="Invoice")
	applicant = fields.Many2one('hr.applicant', string="Applicant")
	contract = fields.Many2one('hr.contract', string="Contract")
	candidate_name = fields.Char(string="Candidate Name")
	month_days_deduction = fields.Boolean(string="Month Days Deduction")
	monthly_deduction = fields.Boolean(string="Monthly Deduction")


	@api.onchange('contract_start_date','no_of_months')
	def get_contract_end_date(self):
		if self.contract_start_date and self.no_of_months:
			self.contract_end_date = self.contract_start_date + (relativedelta(months = self.no_of_months))
		else:
			self.contract_end_date = self.contract_start_date

	@api.onchange('partner_id')
	def test_func(self):
		print (self.partner_id.id)


	# def create_invoice(self):
	#   self.create_journal_entry()
	#   print ("Create Journal Entry")

	# new way of creating invoice START
	def prepare_invoice(self):
		journal = self.env['account.move'].with_context(force_company=self.company_id.id, default_type='out_invoice')._get_default_journal()
		if not journal:
			raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

		invoice_vals = {
			# 'ref': self.client_order_ref or '',
			'ref': self.name,
			'type': 'out_invoice',
			'narration': self.note,
			'currency_id': self.pricelist_id.currency_id.id,
			'campaign_id': self.campaign_id.id,
			'medium_id': self.medium_id.id,
			'source_id': self.source_id.id,
			'invoice_user_id': self.user_id and self.user_id.id,
			'team_id': self.team_id.id,
			'partner_id': self.partner_invoice_id.id,
			'partner_shipping_id': self.partner_shipping_id.id,
			'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
			'invoice_origin': self.name,
			'invoice_date':self.date_invoice,
			'invoice_payment_term_id': self.payment_term_id.id,
			'invoice_payment_ref': self.reference,
			'sale_order_id': self.id,
			'transaction_ids': [(6, 0, self.transaction_ids.ids)],
			'invoice_line_ids': [],
		}
		return invoice_vals


		# old method to create invoice
		# self.create_journal_entry()

	def create_invoice(self):
		invoice_vals_list = []
		invoice_vals = self.prepare_invoice()
		# for line in self.order_line:

		######################################################################################
		edari_product = self.env['product.product'].search([('name','=','Edari Service Fee')],limit=1)

		# Untaxed amounts
		print ("Check1")
		move_lines_list = []
		credit_sum = 0

		lines_not_to_add = []
		if self.date_invoice >= self.contract_start_date and self.date_invoice < self.contract_start_date + (relativedelta(months = 1)):
			lines_not_to_add = ['end']

		elif self.date_invoice >= self.contract_start_date+ (relativedelta(months = 1)) and self.date_invoice < self.contract_end_date - (relativedelta(months = 1)):
			lines_not_to_add = ['end','upfront']

		else:
			lines_not_to_add = ['upfront']

		for line in self.order_line:
			amount = 0
			if line.payment_type == 'interval':
				amount = line.price_unit
			else:
				amount = line.price_subtotal

			if not line.payment_type in lines_not_to_add:

				# qty in months check
				start_plus_qty = self.date_invoice+(relativedelta(months = line.product_uom_qty))
				print 
				# if int(str(start_plus_qty)[5:7]) <= int(str(self.contract_end_date)[5:7]):
				months_differ = relativedelta(start_plus_qty, self.contract_end_date)
				if months_differ.months <= 0:
				# if int(str(start_plus_qty)[5:7]) <= int(str(self.contract_end_date)[5:7]):
					if not line.product_id == edari_product.id:
						# Calculate leave balance
						balance = amount
						if line.leave_deductable:
							temp = self.calculate_leave_balance(balance)
							print ("LLLLLLLLLLLLLLLLLLLLLLLLL")
							print (temp)
							print (balance)
							balance -= temp
							print (balance)
							print ("LLLLLLLLLLLLLLLLLLLLLLLLL")
						invoice_vals['invoice_line_ids'].append(line.prepare_invoice_line(balance,line.product_id.name))
						credit_sum += balance
			if line.product_id == edari_product.id:
				invoice_vals['invoice_line_ids'].append(line.prepare_invoice_line(credit_sum,'Edari Service Fee'))
		#=====================================================================================#


		# invoice_vals['invoice_line_ids'].append((0, 0, line.prepare_invoice_line()))
		# invoice_vals['sale_order_id'] = self.id
		
		if not invoice_vals['invoice_line_ids']:
			raise UserError('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.')

		invoice_vals_list.append(invoice_vals)

		# 3) Create invoices.
		moves = self.env['account.move'].with_context(default_type='out_invoice').create(invoice_vals_list)

		
	# new way of creating invoice ENDS

	##################### Function to calculate leave balance total START #####################
	def calculate_leave_balance(self, balance):
		temp = balance
		no_of_leaves = 0
		for line in self.order_line:
			if line.leave_type:
				employee = self.env['hr.employee'].search([('id','=',self.contract.employee_id.id)])
				leaves = self.env['hr.leave'].search([('employee_id','=',employee.id)])
				for x in leaves:
					if self.date_invoice >= x.request_date_from and self.date_invoice <= x.request_date_to:
						no_of_leaves = x.number_of_days
		return (balance/22)*no_of_leaves




	##################### Function to calculate leave balance total ENDS  #####################

	# @api.onchange('template')
	def get_order_lines(self):
		if self.order_line:
			self.order_line.unlink()
		if self.template:

			code_dict = {}

			salary = self.per_month_gross_salary
			no_months = self.no_of_months
			# order_lines_list = []
			# for y in self.order_line:
			#   print ("XXXXXXXXXXXXXXXXXX")
			#   code_dict[y.code] = y.price_subtotal

			template_tree_recs = self.env['costcard.template.tree'].search([('tree_link','=',self.template.id)], order='handle')
			# for x in self.template.template_tree:
			for x in template_tree_recs:
				global compute_result
				compute_result = 0
				# if ' ' in x.computation_formula:
				# result = eval(x.computation_formula)
				expression = 'global compute_result;\n'+x.computation_formula
				# expression = x.computation_formula
				# expression.replace("result", "cost_card_compute_x1")
				# exec(x.computation_formula)
				try:
					exec(expression)
				except Exception as e:
					raise ValidationError('Error..!\n'+str(e))
				qty = 0
				# if x.costcard_type in ['fixed','calculation']:
				if x.costcard_type in ['manual']:
				# if x.costcard_type:
					qty = self.no_of_months
				# if x.costcard_type == 'manual':
				else:
					qty = 1
					# compute_result = 0

				# order_lines_list.append({
				self.order_line.create({
					'product_id':x.service_name.id,
					# 'sale_order_template_id':self.id,
					'order_id':self.id,
					# 'product_uom_qty':self.no_of_months,
					'product_uom_qty':qty,
					'price_unit':compute_result,
					'leave_type':x.leave_type.id,
					'leave_deductable':x.leave_deductable,
					'leave_deduct_type':x.leave_deduct_type,
					'code':x.code,
					'categ_id':x.service_name.categ_id.id,
					'name':x.code,
					'costcard_type':x.costcard_type,
					'chargable':x.chargable,
					})
				# if x.costcard_type == 'fixed':
				#   code_dict[x.code] = compute_result
				# else:
				# # if x.costcard_type == 'fixed':
				code_dict[x.code] = qty*compute_result
				globals().update(code_dict)
				del compute_result
				# print (order_lines_list)
			# self.order_line = order_lines_list
			# for y in self.order_line:
			# deleting global variables
			for x in code_dict.keys():
				del x

			for x in self.order_line:
				if x.costcard_type == 'calculation':
					print ('XXXXXXXXXXXXXXXXXXX')
					print (x.code)
					x.unlink()



		else:
			self.order_line = None

	def create_edari_fee(self):
		edari_service_charges = self.env['product.product'].search([('name','=','Edari Service Fee')])
		for x in self.order_line:
			if x.product_id.id == edari_service_charges.id:
				x.unlink()
		charable_sum = 0
		for x in self.order_line:
			if x.chargable:
				# charable_sum += x.price_subtotal
				charable_sum += x.price_unit
		if charable_sum > 0:
			edari_service_charges = self.env['product.product'].search([('name','=','Edari Service Fee')])
			price = 0
			if self.percentage > 0:
				price = charable_sum*(self.percentage/100)
			else:
				price = charable_sum
			self.order_line.create({
				'product_id':edari_service_charges.id,
				'name':"Service Charges",
				'code':"SC",
				# 'product_uom_qty':1,
				'product_uom_qty':self.no_of_months,
				'price_unit':price,
				'order_id':self.id,
				'costcard_type':'manual',
				})

	@api.model
	def create(self, vals):
		new_record = super(SaleOrderExt, self).create(vals)
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

		new_record.get_contract_end_date()
				
		
		return new_record

	def write(self, vals):
		rec = super(SaleOrderExt, self).write(vals)
		if 'per_month_gross_salary' in vals:
			self.applicant.salary_expected = vals['per_month_gross_salary']
		return rec


class SOLineExt(models.Model):
	_inherit='sale.order.line'

	code = fields.Char(string="Code")
	chargable = fields.Boolean(string="Chargable")
	manual_amount = fields.Float(string="Manual Amount")
	categ_id = fields.Many2one('product.category', string="Product Category")
	leave_type = fields.Many2one('hr.leave.type', string="Leave Type")
	leave_deductable = fields.Boolean(string="Leave Deductable")
	leave_deduct_type = fields.Selection([
        ('accrued','Accrued'),
        ('non_accrued','Non-Accrued'),
        ], string='Leave Deductable Type', default='accrued')



	def prepare_invoice_line(self,amount,name):
		"""
		Prepare the dict of values to create the new invoice line for a sales order line.
		:param qty: float quantity to invoice
		"""
		self.ensure_one()

		return {
			'display_type': self.display_type,
			'sequence': self.sequence,
			'name': name,
			'product_id': self.product_id.id,
			'product_uom_id': self.product_uom.id,
			'quantity': self.product_uom_qty,
			'discount': self.discount,
			# 'price_unit': self.price_unit,
			'price_unit': amount,
			'tax_ids': [(6, 0, self.tax_id.ids)],
			'analytic_account_id': self.order_id.analytic_account_id.id,
			'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
			'sale_line_ids': [(4, self.id)],
		}

	@api.onchange('manual_amount')
	def get_manual_price_unit(self):
		print ("XXXXXXXXXXXXXXXXXXXXXX")
		print (self.costcard_type)
		print ("XXXXXXXXXXXXXXXXXXXXXX")
		if self.costcard_type == 'manual' and self.order_id.no_of_months>0:
			self.product_uom_qty = self.order_id.no_of_months
			self.price_unit = self.manual_amount/self.order_id.no_of_months
		else:
			self.product_uom_qty = 1
			self.price_unit = 0


	payment_type = fields.Selection([
		('upfront','Upfront'),
		('end','End'),
		('interval','Interval')
		], string='Payment Type', default='upfront')

	costcard_type = fields.Selection([
		('fixed','Fixed'),
		('manual','Manual'),
		('calculation','Calculation'),
		], string='Type', default='manual')
	