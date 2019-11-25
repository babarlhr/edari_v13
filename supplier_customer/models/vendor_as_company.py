from odoo import models, fields, api


class ResPartnerBank(models.Model):
	_inherit = 'res.partner.bank'
	
	iban = fields.Char('IBAN')
	branch_name = fields.Char('Branch Name')
	swift = fields.Char('Swift/Routing Number')


class ResPartner(models.Model):
	_inherit = 'res.partner'
	
	registeration_no = fields.Char('VAT Registeration No', placeholder="e.g TNGBD30285")
	trading_as = fields.Char('Trading As', placeholder="e.g Abbreviated as ...")
	upload_ids = fields.One2many('vendor.documents.upload', 'vendor_id', string='Uploads')
	b_upload_ids = fields.One2many('vendor.bank.documents.upload', 'b_vendor_id', string='Bank Uploads')
	contract_doc_ids = fields.One2many('vendor.contract.upload', 'contract_vendor_id', string='Contract')


class VendorDocumentsUpload(models.Model):
	_name = 'vendor.documents.upload'
	_description = 'Documents'
	
	vendor_id = fields.Many2one('res.partner', 'Vendor')
	# vendor_doc_type = fields.Many2one('vendor.document.type', string='Document')
	vendor_doc_type = fields.Selection([('trade_license', 'Trade License')], default='trade_license', string='Document')
	name = fields.Char('Name')
	relationship = fields.Char('Relationship')
	issue_date = fields.Date('Issue Date')
	expiry_date = fields.Date('Expiry Date')
	issued_by = fields.Selection([
		('ded_dubai', 'DED Dubai'),
		('ded_abu_dhabi', 'DED Abu Dhabi'),
		('outside_uae', 'Outside UAE'),
	], string='Issued By')
	place_of_issue = fields.Char()
	country_of_issue = fields.Many2one('res.country', string='Country Of Issue')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'vendor_document_id', string="Documents")
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class VendorBankDocumentsUpload(models.Model):
	_name = 'vendor.bank.documents.upload'
	_description = 'Documents'
	
	b_vendor_id = fields.Many2one('res.partner', 'Vendor')
	vendor_doc_type = fields.Selection([('bank_letter', 'Bank Letter'), ('vat', 'VAT')], string='Document')
	name = fields.Char('Name')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'b_vendor_document_id', string="Upload Doc")
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break
				

class VendorContractUpload(models.Model):
	_name = 'vendor.contract.upload'
	_description = 'Contract'
	
	contract_vendor_id = fields.Many2one('res.partner', 'Vendor')
	vendor_doc_type = fields.Selection([('contract', 'Contract')], default='contract', string='Document')
	name = fields.Char('Name')
	start_date = fields.Date('Start Date')
	end_date = fields.Date('End Date')
	doc_signed = fields.Selection([
		('yes', 'Yes'),
		('no', 'No'),
	], string='Doc Signed')
	document_count = fields.Integer('Document Count', compute="Compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'contract_document_id', string="Doc Upload")
	
	def Compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class IrAttachment(models.Model):
	_inherit = 'ir.attachment'
	
	vendor_document_id = fields.Many2one('vendor.documents.upload')
	contract_document_id = fields.Many2one('vendor.contract.upload')
	b_vendor_document_id = fields.Many2one('vendor.bank.documents.upload')
