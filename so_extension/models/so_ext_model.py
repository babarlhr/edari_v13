# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class SaleOrderExt(models.Model):
	_inherit='sale.order'

	no_of_months = fields.Integer(string="No of Months")
	per_month_gross_salary = fields.Float(string="Per Month Gross Salary")
	template = fields.Many2one('costcard.template', string="Template")

	def get_order_lines(self):
		self.order_line.unlink()
		if self.template:
			global compute_result
			salary = self.per_month_gross_salary
			no_months = self.no_of_months
			order_lines_list = []
			for temp in self.template.template_tree:
				expression = 'global compute_result;\n'+temp.computation_formula
				exec(expression)
				self.order_line.create({
					'product_id':temp.service_name.id,
					'name':temp.service_name.id,
					'product_uom_qty':self.no_of_months,
					'price_unit':compute_result,
					'order_id':self.id,
					})
		else:
			self.order_line = None
