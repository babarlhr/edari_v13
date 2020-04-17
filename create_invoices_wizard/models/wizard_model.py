# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class CreateInvWizard(models.Model):
	_name = 'create.invoice.wizard'
	_description = "This class is of a wizard that will give option to create invoices of a selected month."

	month = fields.Date(string="Invoice Month")


	def confirm(self):
		active_invoices =self.env['sale.order'].browse(self._context.get('active_ids'))
		to_invoice = active_invoices.search([('state','=','done'),('contract_start_date','<=',self.month),('contract_end_date','>=',self.month),('costcard_type','=',"cost_card")])
		
		for index in to_invoice:
			if index.contract.state == "open":
				print (index)
				index.create_invoice(self.month)
				index.state = "sale"
				index.date_invoice = self.month
				index.state = "done"