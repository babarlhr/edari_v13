# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class HrContractExtension(models.Model):
	_inherit = 'hr.contract'

	contract_length = fields.Char("Contract Length")

	@api.depends('employee_id.cost_card')
	def get_wage(self):
		for x in self:
			if x.employee_id:
				if x.employee_id.cost_card:
					x.wage = x.employee_id.cost_card.per_month_gross_salary
	