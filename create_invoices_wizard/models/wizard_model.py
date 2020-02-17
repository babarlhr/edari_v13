# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class CreateInvWizard(models.Model):
	_name = 'create.invoice.wizard'
	_description = "This class is of a wizard that will give option to create invoices of a selected month."

	month = fields.Date(string="Invoice Month")


	def confirm(self):
		so_recs = self.env['sale.order'].search([('contract.state','=','open')])
		for index in so_recs:
			try:
				if not index.date_invoice:
					raise ValidationError("Invoice Date Not Available!")
				if not index.contract_start_date:
					raise ValidationError("Contract Start Date Not Available!")
				if not index.contract_end_date:
					raise ValidationError("contract End Date Not Available!")
				if index.date_invoice.month == self.month.month and index.date_invoice.year == self.month.year:
					index.create_invoice()
			except Exception as e:
				raise ValidationError("Cost Card: "+index.name+"\n"+str(e))


		