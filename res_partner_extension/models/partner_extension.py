# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class PartnerExtension(models.Model):
	_inherit='res.partner'

	trade_license_no = fields.Char("Trade License No")
	trading_as = fields.Char("Trading as")

	# billing details fields
	trade_license_no_bill = fields.Char("Trade License Number")
	branch_name = fields.Char("Branch Name")
	beneficiary_name = fields.Char("Beneficiary Name")
	account_number = fields.Char("Account Number")
	iban = fields.Char("IBAN")
	swift_or_route = fields.Char("SWIFT or Routing Number")
	vat = fields.Char("VAT")
	vat_reg_no = fields.Char("VAT Registration Number")
	billing_address = fields.Char("Billing Address")
	address_line_1 = fields.Char("Address line 1")
	address_line_2 = fields.Char("Address line 2")
	city_emirate = fields.Char("City/Emirate")
	po_box = fields.Char("PO Box")



	document_tree = fields.One2many('document.tree', 'partner_link')
	