# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError

from datetime import datetime
from dateutil.relativedelta import relativedelta


class AccMoveExt(models.Model):
	_inherit='account.move'

	sale_order_id = fields.Many2one('sale.order',string="Sale Order")
	employee = fields.Many2one('hr.employee', string="Employee")
	automated_invoice = fields.Boolean(string = "Automated Invoice")
	invoice_month = fields.Date(string= "Invoice Month")
	from_date = fields.Date(string= "From Date")
	to_date = fields.Date(string= "To Date")

	pro_rate_adjust = fields.Float(string= "Pro Rate Adjustment")
	leave_taken = fields.Float(string= "Leave Taken")
	sick_days_taken = fields.Float(string= "Sick Days Taken")

	report_name = fields.Char(string= "Report Name", compute = "UpdateReportName")
	invoice_requester = fields.Many2one('res.partner',string="Invoice Requester")

	def UpdateReportName(self):
		for rec in self:
			if rec.invoice_date:
				if rec.partner_id.trading_as:
					customer_name = rec.partner_id.trading_as
				else:
					customer_name = rec.partner_id.name[:3]
				oldformat = str(rec.invoice_date)
				dateobject = datetime.strptime(oldformat,'%Y-%m-%d')
				month = dateobject.strftime('%m')
				year = dateobject.strftime('%Y')
				rec.report_name = str(customer_name) + '-' + str(rec.name) + '-' + str(month) + '-' + str(year) 


	@api.onchange('partner_id')
	def get_payment_term(self):
		if self.partner_id:
			self.invoice_payment_term_id = self.partner_id.property_payment_term_id.id
		else:
			self.invoice_payment_term_id = False


	@api.onchange('sale_order_id')
	def get_invoice_requester(self):
		if self.sale_order_id:
			self.invoice_requester = self.sale_order_id.invoice_requester.id
		else:
			self.invoice_requester = False

class ProductExtension(models.Model):
	_inherit='product.product'

	accruing_account_id = fields.Many2one('account.account',string = "Accrued Account")


# class PartnerExtensionSo(models.Model):
# 	_inherit='res.partner'

# 	function_contact = fields.Selection([
# 		('primary','Primary'),
# 		('billing','Billing'),
# 		], string='Function', default="primary")
