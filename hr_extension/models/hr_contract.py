# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class HrContractExtension(models.Model):
	_inherit = 'hr.contract'

	contract_length = fields.Char("Contract Length")
	cost_card = fields.Many2one('sale.order',"Cost Card")

	@api.depends('employee_id.cost_card')
	def get_wage(self):
		for x in self:
			if x.employee_id:
				if x.employee_id.cost_card:
					x.wage = x.employee_id.cost_card.per_month_gross_salary


	def write(self,vals):
		rec = super(HrContractExtension,self).write(vals)
		if 'state' in vals and vals['state'] == 'open':
			so_rec = self.env['sale.order'].search([('id','=',self.cost_card.id)])
			if so_rec:
				so_rec.write({
					'contract_start_date':self.date_start,
					'contract_start_date':self.date_end,
					'contract_state':self.state,
						})
		return rec


		