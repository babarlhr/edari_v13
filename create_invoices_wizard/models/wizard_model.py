# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class CreateInvWizard(models.Model):
	_name = 'create.invoice.wizard'
	_description = "This class is of a wizard that will give option to create invoices of a selected month."

	month = fields.Date(string="Invoice Month")


	def confirm(self):
		so_recs = self.env['sale.order'].search([('state','=','sale'),('contract_start_date','<=',self.month),('contract_end_date','>=',self.month)])
		print ("-----------------")
		print (so_recs)
		print ("-----------------")
		for index in so_recs:
			if index.contract.state == "open":
				print (index)
				index.create_invoice(self.month)


		