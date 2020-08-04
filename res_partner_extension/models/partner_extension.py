# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class PartnerExtension(models.Model):
	_inherit='res.partner'

	trade_license_no = fields.Char("Trade License No")
	trading_as = fields.Char("Trading as")
	# employee_check = fields.Boolean("Employee")

	# billing details fields
	trade_license_no = fields.Char("Trade License Number")
	function_contact = fields.Selection([
		('primary','Primary'),
		('billing','Billing'),
		# ('inv_requestor','Invoice Requestor'),
		# ('inv_buyer','Invoice Buyer'),
		], string='Function', default="primary")
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
	default_edari_percentage = fields.Float(string="Default Edari Percentage" ,digits=(4,4))
	client_owner = fields.Many2one('hr.employee', string='Client Owner')

	inv_attention = fields.Char("Invoice Attention")


	document_tree = fields.One2many('document.tree', 'partner_link')


	@api.onchange('document_tree')
	def CountDocuments(self):
		unique_docs = []
		for doc in self.document_tree:
			if doc.document_type not in unique_docs:
				unique_docs.append(doc.document_type)

		for ud in unique_docs:
			count = 0
			for docu in self.document_tree:
				if docu.document_type.id == ud.id:
					count += 1

			for x in self.document_tree:
				if x.document_type.id == ud.id:
					x.doc_count = count 



	@api.onchange('company_type')
	def null_function_contact(self):
		if self.company_type == 'company':
			self.function_contact = False



	def CantCreateCompany(self):
		current_user_id = self.env.uid
		current_user = self.env['res.users'].search([('id','=',current_user_id)])

		if current_user.has_group('res_partner_extension.cannot_create_company'):
			if self.company_type == 'company':
				raise ValidationError("You are not allowed to create a company, please contact your system adminstrator")

	def CantCreateEditVendor(self):
		for rec in self:
			current_user_id = self.env.uid
			current_user = self.env['res.users'].search([('id','=',current_user_id)])

			if current_user.has_group('res_partner_extension.cannot_create_edit_vendor'):
				if rec.supplier_rank > 0:
					raise ValidationError("You are not allowed to create or edit a vendor, please contact your system adminstrator")

	@api.model
	def create(self, vals):
		new_record = super(PartnerExtension, self).create(vals)
		# updating wage in contract
		new_record.CantCreateCompany()
		new_record.CantCreateEditVendor()


		current_user_id = self.env.uid
		current_user = self.env['res.users'].search([('id','=',current_user_id)])

		if current_user.has_group('res_partner_extension.cannot_create_contact'):
			raise ValidationError("You are not allowed to create a contact, please contact your system adminstrator")
		
		return new_record

	def write(self,vals):

		# status_before = self.company_type
		rec = super(PartnerExtension,self).write(vals)
		# status_after = self.company_type
		# if status_after != status_before:
		if "company_type" in vals:
			current_user_id = self.env.uid
			current_user = self.env['res.users'].search([('id','=',current_user_id)])

			if current_user.has_group('res_partner_extension.cannot_create_company'):
				raise ValidationError("You are not allowed to create a company, please contact your system adminstrator")
		self.CantCreateEditVendor()
		return rec



class BankExt(models.Model):
	_inherit='res.bank'

	swift = fields.Char("SWIFT")
	