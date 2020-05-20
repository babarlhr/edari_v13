# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError



class SaleOrderExt(models.Model):
	_inherit='sale.order'

	no_of_months = fields.Integer(string="No of Months")
	per_month_gross_salary = fields.Float(string="Per Month Gross Salary")
	template = fields.Many2one('costcard.template', string="Template")
	job_pos = fields.Many2one('hr.job', string="Job Position")
	version = fields.Integer(string="Version No")



	# @api.onchange('template')
	def get_order_lines(self):
		if self.template:

			code_dict = {}

			salary = self.per_month_gross_salary
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
				if x.fixed:
					qty = 1
				else:
					qty = self.no_of_months
				# order_lines_list.append({
				self.order_line.create({
					'product_id':x.service_name.id,
					# 'sale_order_template_id':self.id,
					'order_id':self.id,
					'product_uom_qty':self.no_of_months,
					'price_unit':compute_result,
					'code':x.code,
					'name':x.code,
					})
				code_dict[x.code] = self.no_of_months*compute_result
				globals().update(code_dict)
				del compute_result
				print ("77777777777777777777777")
				# print (order_lines_list)
				print ("88888888888888888888888")
			# self.order_line = order_lines_list
			# for y in self.order_line:
			# deleting global variables
			for x in code_dict.keys():
				del x
		else:
			print ("9999999999999999999999")
			self.order_line = None
			print ("00000000000000000000000000000000")


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