# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class CreateInvWizard(models.Model):
	_name = 'create.invoice.wizard'
	_description = "This class is of a wizard that will give option to create invoices of a selected month."

	month = fields.Date(string="Invoice Month")


	def confirm(self):

		invoice_ids = []
		active_invoices =self.env['sale.order'].browse(self._context.get('active_ids'))
		
		for index in active_invoices:
			if index.state == "done" and index.contract.state == "open" and index.costcard_type == "cost_card": 
				if index.contract_start_date.replace(day=1) <= self.month.replace(day=1) <= index.contract_end_date.replace(day=1):
					create_invoice = True			
					
					invoices = self.env['account.move'].search([('sale_order_id','=',index.id)])
					for inv in invoices:
						if inv.invoice_date.replace(day=1) == self.month.replace(day=1):
							create_invoice = False
					
					if create_invoice == True:
						invoice_id = index.create_invoice(self.month)
						index.state = "sale"
						index.date_invoice = self.month
						index.state = "done"
						invoice_ids.append(invoice_id.id)

		# print (invoice_ids)


		return {
			'res_model': 'account.move',
			'type': 'ir.actions.act_window',
			'view_mode': 'list,form',
			'name':'Generated Invoices',
			'view_type': 'form',
			'target': 'current',
			'domain': [('id','in',invoice_ids)],
			}