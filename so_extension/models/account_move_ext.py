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



class ProductExtension(models.Model):
	_inherit='product.product'

	accruing_account_id = fields.Many2one('account.account',string = "Accrued Account")


# class PartnerExtensionSo(models.Model):
# 	_inherit='res.partner'

# 	function_contact = fields.Selection([
# 		('primary','Primary'),
# 		('billing','Billing'),
# 		], string='Function', default="primary")
