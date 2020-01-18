# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError

from datetime import datetime
from dateutil.relativedelta import relativedelta


class SaleOrderExt(models.Model):
	_inherit='sale.order'

	no_of_months = fields.Integer(string="No of Months")
	per_month_gross_salary = fields.Float(string="Per Month Gross Salary")
	template = fields.Many2one('costcard.template', string="Template")
	job_pos = fields.Many2one('hr.job', string="Job Position")
	version = fields.Integer(string="Version No")
	interval = fields.Integer(string="Interval")
	contract_start_date = fields.Date(string="Contract Start Date")
	contract_end_date = fields.Date(string="Contract End Date")
	date_invoice = fields.Date(string="Invoice Date")
	invoice_amount = fields.Float(string="Invoice Amount")
	percentage = fields.Float(string="Percentage %")
	invoice_id = fields.Many2one('account.move', string="Invoice")


	@api.onchange('contract_start_date','interval')
	def get_contract_end_date(self):
		if self.contract_start_date and self.interval:
			self.contract_end_date = self.contract_start_date + (relativedelta(months = self.interval))
		else:
			self.contract_end_date = self.contract_start_date

	def create_invoice(self):
		self.create_journal_entry()


	def create_journal_entry(self):
		self.create_journal_entry_form()
		line_ids = self.generate_entry_lines()
		self.invoice_id.line_ids = line_ids
		# self.create_journal_entry_form(line_ids)

	def generate_entry_lines(self):

		# Untaxed amounts
		print ("Check1")
		move_lines_list = []
		# credit_account = self.env['account.account'].search([], limit=1)
		debit_account = self.partner_id.property_account_receivable_id.id
		move_lines_list.append(self.create_entry_lines(debit_account,self.amount_untaxed,0,'Untaxed amount credit'))
		for x in self.order_line:

			move_lines_list.append(self.create_entry_lines(x.product_id.property_account_income_id.id,0,x.price_subtotal,'Untaxed amount Debit'))

		if self.amount_tax > 0:
		# taxes
			move_lines_list.append(self.create_entry_lines(debit_account,self.amount_tax,0,'Taxed amount credit'))
			move_lines_list.append(self.create_entry_lines(self.partner_id.property_account_receivable_id.id,0,self.amount_tax,'Taxed amount Debit'))
		return move_lines_list

	# def create_entry_lines(self,account,debit,credit,entry_id,name):
	def create_entry_lines(self,account,debit,credit,name):
		if debit > 0 or credit > 0:
			# self.env['account.move.line'].create({
			return{
					'account_id':account,
					'partner_id':self.partner_id.id,
					'name':name,
					'debit':debit,
					'credit':credit,
					'move_id':self.invoice_id.id,
					}

	def create_journal_entry_form(self):
		journal_entries = self.env['account.move']
		journal = self.env['account.journal'].search([], limit=1)
		journal_entries_lines = self.env['account.move.line']

		if not self.invoice_id:   
			create_journal_entry = journal_entries.create({
					'journal_id': journal.id,
					'date':self.date_invoice,
					# 'line_ids': line_ids,
					'ref' : self.name,
					# 'ref' : "Test",
					})

			self.invoice_id = create_journal_entry.id
			journal_entry = create_journal_entry
		else:
			
			journal_entry = self.invoice_id
			self.invoice_id.journal_id = journal.id
			self.invoice_id.date = self.date_invoice
			self.invoice_id.ref = self.name

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
			# 	print ("XXXXXXXXXXXXXXXXXX")
			# 	code_dict[y.code] = y.price_subtotal

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
				# if x.costcard_type in ['fixed','manual']:
				if x.costcard_type:
					qty = 1
				# if x.costcard_type == 'manual':
				else:
					qty = self.no_of_months
					# compute_result = 0

				# order_lines_list.append({
				self.order_line.create({
					'product_id':x.service_name.id,
					# 'sale_order_template_id':self.id,
					'order_id':self.id,
					# 'product_uom_qty':self.no_of_months,
					'product_uom_qty':qty,
					'price_unit':compute_result,
					'code':x.code,
					'name':x.code,
					'costcard_type':x.costcard_type,
					'chargable':x.chargable,
					})
				# if x.costcard_type == 'fixed':
				# 	code_dict[x.code] = compute_result
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
				'product_uom_qty':1,
				'price_unit':price,
				'order_id':self.id,
				'costcard_type':'manual',
				})



	@api.model
	def create(self, vals):
		new_record = super(SaleOrderExt, self).create(vals)
		records = self.env['sale.order'].search([], order='version desc')
		if records:
			# print (records[0].)
			new_record.version = records[0].version+1
		
		return new_record


	# @api.multi
	# def write(self, vals):
	# 	rec = super(SaleOrderExt, self).write(vals)
	# 	return rec


class SOLineExt(models.Model):
	_inherit='sale.order.line'

	code = fields.Char(string="Code")
	chargable = fields.Boolean(string="Chargable")
	manual_amount = fields.Float(string="Manual Amount")

	@api.onchange('manual_amount')
	def get_manual_price_unit(self):
		if self.order_id.no_of_months>0:
			self.price_unit = self.manual_amount/self.order_id.no_of_months
		else:
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
    