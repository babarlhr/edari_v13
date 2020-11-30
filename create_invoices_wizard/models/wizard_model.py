# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError, UserError


class CreateInvWizard(models.Model):
	_name = 'create.invoice.wizard'
	_description = "This class is of a wizard that will give option to create invoices of a selected month."

	month = fields.Date(string="Invoice Month")
	invoice_date = fields.Date(string="Invoice Date")
	flag_reasons = fields.Boolean()
	skip_reason_lines = fields.One2many('skipping.reasons','invoice_wizard_id')


	def confirm(self):

		create_reason = self.env['skipping.reasons']
		skip_reasons = ""
		skip_lines = []
		invoice_ids = []
		active_invoices =self.env['sale.order'].browse(self._context.get('active_ids'))
		
		for index in active_invoices:

			if index.state == "done" and index.contract.state == "open" and index.costcard_type == "cost_card" and index.so_type == "cost_card":
				if index.contract_start_date.replace(day=1) <= self.month.replace(day=1) <= index.contract_end_date.replace(day=1):
					create_invoice = True		
					
					invoices = self.env['account.move'].search([('sale_order_id','=',index.id)])
					for inv in invoices:
						if inv.invoice_month:
							if inv.invoice_month.replace(day=1) == self.month.replace(day=1):
								create_invoice = False
					
					if create_invoice == True:
						try:
							invoice_id = index.create_invoice(self.month,self.invoice_date)
							index.state = "sale"
							index.date_invoice = self.month
							index.state = "done"
							invoice_ids.append(invoice_id.id)
						except UserError as e:
							skip_reasons = str(e)
						except ValidationError as e:
							skip_reasons = str(e)
					else:
						skip_reasons = "Invoice Already Created for this month"

				else:
					skip_reasons = "Invoice Month is not in the range of contract"
			else:
				if index.state != "done":
					skip_reasons = "Cost card is not locked"
				if index.contract.state != "open":
					skip_reasons = "Contract is not in running state"
				if index.costcard_type != "cost_card":
					skip_reasons = "Cost Card type is not Cost Card"
				if index.so_type != "cost_card":
					skip_reasons = "Cost Card type is not Cost Card"
				
			have_a_reason = False
			line_created = ""
			if skip_reasons:	
				line_created =create_reason.create({
					'cost_card_number':index.name,
					'skip_reason':skip_reasons,
					'invoice_wizard_id':self.id
					})
			if line_created:
				have_a_reason = True

		if self.flag_reasons == False and have_a_reason == True:
			self.flag_reasons = True
			return {
		        'context': self.env.context,
		        'view_type': 'form',
		        'view_mode': 'form',
		        'res_model': 'create.invoice.wizard',
		        'name':'Create Cost Card Invoices',
		        'res_id': self.id,
		        'view_id': False,
		        'type': 'ir.actions.act_window',
		        'target': 'new',
		    }
		else:
			return {
			'res_model': 'account.move',
			'type': 'ir.actions.act_window',
			'view_mode': 'list,form',
			'name':'Generated Invoices',
			'view_type': 'form',
			'target': 'current',
			'domain': [('id','in',invoice_ids)],
			}


class SkippingReasons(models.Model):
	_name = 'skipping.reasons'

	cost_card_number = fields.Char()
	skip_reason = fields.Char()
	invoice_wizard_id = fields.Many2one('create.invoice.wizard')
