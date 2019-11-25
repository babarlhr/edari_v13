from odoo import models, fields, api


class ResPartnerDependent(models.Model):
	_inherit = 'res.partner'
	_description = 'Dependent'

	vendor_id = fields.Many2one('res.partner', string='Parent')
	relationship = fields.Selection([
		('spouse', 'Spouse'),
		('parent', 'Parent'),
		('child', 'Child'),
		('other', 'Other'),
	], string='Relationship', default='', required=False)
	comment = fields.Text()
	

class ResPartner(models.Model):
	_inherit = 'res.partner'

	customer = fields.Boolean(string='Is a Customer', default=False,
							   help="Check this box if this contact is a customer.")
	dependent_ids = fields.One2many('res.partner', 'vendor_id', string='Dependents')
	name_in_passport = fields.Char('Name as per Passport/Emirates ID', translate=True)
	nationality = fields.Many2one('res.country', string='Nationality')
	date_of_birth = fields.Date('Date of birth')
	uae_visa_held = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='UAE Visa held')
	education_level = fields.Selection([
		('high_school', 'High School'),
		("bachelors", "Bachelors"),
		('master', 'Master'),
		('phd', 'Phd'),
	], string='Level of education')
	university = fields.Char('University')
	uni_country = fields.Many2one('res.country', string='Country')
	year_of_graduation = fields.Selection(
		selection="compute_years", string="Year of graduation", store=True)
	marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string='Marital status')
	children_dependent = fields.Selection([
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
	])
	client_email = fields.Char('Client Email')
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
	cv_upload_ids = fields.One2many('cv.document.upload', 'cv_vendor_id', string='CV Upload')
	
	# Passport section
	passport_issue_country_id = fields.Many2one('res.country', 'Country of issue')
	passport_number = fields.Char('Passport Number')
	passport_upload_ids = fields.One2many('passport.vendor.documents.upload', 'p_vendor_id', string='Uploads')
	
	# Emirates ID
	emirates_upload_ids = fields.One2many('emirates.vendor.documents.upload', 'e_vendor_id', string='Uploads')
	
	# Education Certificate
	edu_degree_attested = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Degree Attested in UAE')
	edu_mofa_attestation = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='MOFA Attestation')
	edu_upload_ids = fields.One2many('edu.vendor.documents.upload', 'edu_vendor_id', string='Uploads')
	
	# Medical Insurance Card/ Policy
	insur_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Medical Insurance Required?')
	insur_for_dependents_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='MED Insurance for dependents required?')
	insur_notes = fields.Text('Note:')
	insurance_upload_ids = fields.One2many('insur.vendor.documents.upload', 'insur_vendor_id', string='Uploads')

	# Visa
	visa_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Visa Required?')
	labour_card_required = fields.Selection([
		('yes', 'Yes'),
		('no', 'No'),
	], string='If Labour card Only NOC Uploaded:')
	family_visa_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Family Visa Required?')
	visa_upload_ids = fields.One2many('visa.vendor.documents.upload', 'visa_vendor_id', string='Uploads')

	# Visa Process
	vp_application_type = fields.Selection([
		('in_country', 'In Country'),
		('out_country', 'Out of country'),
		('labour_card', 'Labour Card'),
	], string='Application type')
	vp_labour_card_required = fields.Selection([
		('yes', 'Yes'),
		('no', 'No'),
	], string='If Labour card Only NOC Uploaded:')
	vp_basic = fields.Float('Basic')
	vp_house_allowance = fields.Float('House Allowance')
	other_allowance = fields.Float('Other Allowance')
	probation_period = fields.Selection([
		('3_months', '3 Months'),
		('6_months', '6 Months'),
	], string='Probation Period')
	attested_degree = fields.Selection([
		('yes', 'Yes'),
		('no', 'No'),
	], string='Attested Degree')
	vp_profession = fields.Char('Profession')
	vp_upload_ids = fields.One2many('vp.vendor.documents.upload', 'vp_vendor_id', string='Uploads')

	# Employment Agreements
	emp_contract_name = fields.Char('Name:')
	emp_nationality = fields.Many2one('res.country', string='Nationality:')
	emp_passport_no = fields.Char('Passport number:')
	emp_upload_ids = fields.One2many('emp.vendor.documents.upload', 'emp_vendor_id', string='Uploads')
	
	# Commercial Agreements
	commercial_contract_name = fields.Char('Name:')
	commercial_nationality = fields.Many2one('res.country', string='Nationality:')
	commercial_passport_no = fields.Char('Passport number:')
	commercial_upload_ids = fields.One2many('commercial.vendor.documents.upload', 'commercial_vendor_id', string='Uploads')
	
	def compute_years(self):
		year_list = []
		for i in range(2000, 2100):
			year_list.append((str(i), str(i)))
		return year_list
	
	def add_passport_dependents_info(self):
		dependent_ids = self.dependent_ids
		vals = []
		res_id = self.env['passport.vendor.documents.upload'].search([
			('person_id', '=', self.id), ('p_vendor_id', '=', self.id)])
		if not res_id:
			vals.append({
				'p_vendor_id': self.id,
				'person_id': self.id,
				'document': 'passport',
				'relationship': 'candidate',
				'date_of_birth': self.date_of_birth,
				'gender': self.gender,
			})
		else:
			res_id.update({
				'document': 'passport',
				'relationship': 'candidate',
				'date_of_birth': self.date_of_birth,
				'gender': self.gender,
			})
		for dependent in dependent_ids:
			res_id = self.env['passport.vendor.documents.upload'].search([
				('person_id', '=', dependent.id), ('p_vendor_id', '=', self.id)])
			if not res_id:
				vals.append({
					'p_vendor_id': self.id,
					'person_id': dependent.id,
					'document': 'passport',
					'relationship': dependent.relationship,
					'date_of_birth': dependent.date_of_birth,
					'gender': dependent.gender,
				})
			else:
				res_id.update({
					'document': 'passport',
					'relationship': dependent.relationship,
					'date_of_birth': dependent.date_of_birth,
					'gender': dependent.gender,
				})
		self.env['passport.vendor.documents.upload'].create(vals)
		
	def add_emirate_dependents_info(self):
		dependent_ids = self.dependent_ids
		vals = []
		res_id = self.env['emirates.vendor.documents.upload'].search([
			('person', '=', self.id), ('e_vendor_id', '=', self.id)])
		if not res_id:
			vals.append({
				'e_vendor_id': self.id,
				'person': self.id,
				'document': 'emirate_id',
				'relationship': 'candidate',
			})
		else:
			res_id.update({
				'document': 'emirate_id',
				'relationship': 'candidate',
			})
		for dependent in dependent_ids:
			res_id = self.env['emirates.vendor.documents.upload'].search([
				('person', '=', dependent.id), ('e_vendor_id', '=', self.id)])
			if not res_id:
				vals.append({
					'e_vendor_id': self.id,
					'person': dependent.id,
					'document': 'emirate_id',
					'relationship': dependent.relationship,
				})
			else:
				res_id.update({
					'document': 'emirate_id',
					'relationship': dependent.relationship,
				})
		self.env['emirates.vendor.documents.upload'].create(vals)


class CvVendorUpload(models.Model):
	_name = 'cv.document.upload'
	
	cv_vendor_id = fields.Many2one('res.partner', string='Vendor')
	person_id = fields.Many2one('res.partner', 'Name')
	document = fields.Selection([('cv', 'CV')], default='cv', string='Document')
	relationship = fields.Selection([
		('candidate', 'Candidate'),
	], default='candidate', string='Relationship')
	document_count = fields.Integer('Document Count', compute="Compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'cv_vendor_document_id', string="Documents")
	
	def Compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class PassportVendorDocumentsUpload(models.Model):
	_name = 'passport.vendor.documents.upload'
	_description = 'Documents'
	
	p_vendor_id = fields.Many2one('res.partner', 'Vendor')
	person_id = fields.Many2one('res.partner', 'Person')
	document = fields.Selection([('passport', 'Passport')], default='passport', string='Document')
	relationship = fields.Selection([
		('candidate', 'Candidate'),
		('spouse', 'Spouse'),
		('parent', 'Parent'),
		('child', 'Child'),
		('other', 'Other'),
	], 'Relationship')
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
	date_of_birth = fields.Date('Date of birth')
	passport_number = fields.Char('Passport No')
	issue_date = fields.Date('Issue Date')
	expiry_date = fields.Date('Expiry Date')
	passport_issue_country_id = fields.Many2one('res.country', 'Country of issue')
	document_count = fields.Integer('Document Count', compute="Compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'p_vendor_document_id', string="Documents")
	
	def Compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class EmiratesVendorDocumentsUpload(models.Model):
	_name = 'emirates.vendor.documents.upload'
	_description = 'Emirate ID Document'
	
	e_vendor_id = fields.Many2one('res.partner', 'Vendor')
	person = fields.Many2one('res.partner', 'Name')
	document = fields.Selection([('emirate_id', 'Emirate ID')], default='emirate_id', string='Document')
	relationship = fields.Selection([
		('candidate', 'Candidate'),
		('spouse', 'Spouse'),
		('parent', 'Parent'),
		('child', 'Child'),
		('other', 'Other'),
	], 'Relationship')
	emirate_id_no = fields.Char('Emirates ID No')
	issue_date = fields.Date('Issue Date')
	expiry_date = fields.Date('Expiry Date')
	nationality = fields.Many2one('res.country', string='Nationality')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'e_vendor_document_id', string="Documents")
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class EduVendorDocumentsUpload(models.Model):
	_name = 'edu.vendor.documents.upload'
	_description = 'Edu Document'
	
	edu_vendor_id = fields.Many2one('res.partner', 'Vendor')
	person = fields.Many2one('res.partner', 'Name')
	edu_relationship = fields.Selection([
		('candidate', 'Candidate'),
	], 'Relationship')
	document = fields.Selection([
		('bachelors', 'Bachelors'),
		('bachelors_attested', 'Bachelors Attested'),
		('master', 'Master'),
		('master_attested', 'Master Attested'),
		('phd', 'Phd'),
		('phd_attested', 'Phd Attested'),
	], string='Document')
	edu_university = fields.Char('University / School')
	edu_year_of_graduation = fields.Selection(string='Graduation Year', selection='compute_years', store=True)
	edu_country_id = fields.Many2one('res.country', string='Country')
	edu_degree_type = fields.Selection([
		('economics', 'Economics'),
		('science', 'Sciences Engineering'),
		('other', 'Other'),
	], string='Degree Type')
	edu_degree_attested = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Degree Attested in UAE')
	edu_mofa_attestation = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='MOFA Attestation')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'edu_vendor_document_id', string="Documents")

	def compute_years(self):
		year_list = []
		for i in range(2000, 2100):
			year_list.append((str(i), str(i)))
		return year_list
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class InsurVendorDocumentsUpload(models.Model):
	_name = 'insur.vendor.documents.upload'
	_description = 'Documents'
	
	insur_vendor_id = fields.Many2one('res.partner', 'Vendor')
	document = fields.Selection([
		('med_ins_policy', 'Med Ins Policy (Current/ Own)'),
		('med_ins_policy_edari', 'Med Ins Policy (Edari)'),
		('maf', 'MAF'),
		('maf_signed', 'MAF (Signed)'),
		('supporting_documents', 'Supporting Documents'),
	], string='Document')
	person = fields.Many2one('res.partner', 'Name')
	relationship = fields.Selection([
		('candidate', 'Candidate'),
		('spouse', 'Spouse'),
		('parent', 'Parent'),
		('child', 'Child'),
		('other', 'Other'),
	], 'Relationship')
	insurer = fields.Char('Insurer')
	policy_no = fields.Char('Policy No')
	issue_date = fields.Date('Issue Date')
	expiry_date = fields.Date('Expiry Date')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'insur_vendor_document_id', string="Documents")
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class VisaVendorDocumentsUpload(models.Model):
	_name = 'visa.vendor.documents.upload'
	_description = 'Visa Document'
	
	visa_vendor_id = fields.Many2one('res.partner', 'Vendor')
	person = fields.Many2one('res.partner', 'Name')
	document = fields.Selection([
		('visa_previous_emp', 'Visa (Previous Employer)'),
		('edari_visa', 'Edari Visa'),
	], string='Document')
	relationship = fields.Selection([
		('candidate', 'Candidate'),
		('spouse', 'Spouse'),
		('parent', 'Parent'),
		('child', 'Child'),
		('other', 'Other'),
	], 'Relationship')
	visa_uid = fields.Char('UID')
	visa_issue_date = fields.Date('Issue Date')
	visa_expiry_date = fields.Date('Expiry Date')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'visa_vendor_document_id', string="Documents")
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class VPVendorDocumentsUpload(models.Model):
	_name = 'vp.vendor.documents.upload'
	_description = 'Documents'
	
	vp_vendor_id = fields.Many2one('res.partner', 'Vendor')
	person = fields.Many2one('res.partner', 'Name')
	document = fields.Selection([
		('noc', 'NOC'),
		('labour_offer', 'Labour Offer'),
		('labour_offer_signed', 'Labour Offer Signed'),
		('labour_contract', 'Labour Contract'),
		('labour_contract_signed', 'Labour Contract Signed'),
		('entry_permit', 'Entry Permit'),
		('work_permit', 'Work Permit'),
	], string='Document')
	relationship = fields.Selection([
		('candidate', 'Candidate'),
	], 'Relationship')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'vp_vendor_document_id', string="Documents")
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break


class EmpVendorDocumentsUpload(models.Model):
	_name = 'emp.vendor.documents.upload'
	_description = 'Contract Document'
	
	emp_vendor_id = fields.Many2one('res.partner', 'Vendor')
	relationship = fields.Selection([
		('candidate', 'Candidate'),
	], 'Relationship')
	person = fields.Many2one('res.partner', 'Name')
	document_name = fields.Char('Document_name', default='Employment')
	document = fields.Selection([
		('word_file', 'Word File'),
		('signed_edari_countersigned', 'Signed (Edari) Countersigned'),
	], string='Document')
	contract_date = fields.Date('Contract Date')
	job_title = fields.Char('Job Title')
	client_name = fields.Char('Client Name')
	client_contract = fields.Char('Client Contact')
	site_location = fields.Selection([('dubai', 'Dubai'), ('abu_dhabi', 'Abu Dhabi')], string='Site Location')
	basic_salary = fields.Float('Basic Salary')
	housing_allowance = fields.Float('Housing Allowance')
	other_allowances = fields.Float('Other Allowances')
	start_date = fields.Date('Start Date')
	end_date = fields.Date('End Date')
	duration = fields.Selection([
		('3', '3 Months'),
		('6', '6 Months'),
		('12', '12 Months'),
		('18', '18 Months'),
		('24', '24 Months'),
	], string='Duration')
	probation_period = fields.Selection([
		('3', '3 Months'),
		('6', '6 Months'),
	], string='Probation Period')
	medical = fields.Selection([
		('single', 'Single Status'),
		('family', 'Family Status'),
	], string='Medical')
	annual_ticket = fields.Selection([
		('single', 'Single Status'),
		('family', 'Family Status'),
	], string='Medical')
	medical_cost = fields.Float('Medical Cost')
	special_provision = fields.Char('Special Provisions')
	annual_ticket_cost = fields.Float('Annual Ticket Cost')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'ag_vendor_document_id', string="Documents")
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break
				

class CommercialVendorDocumentsUpload(models.Model):
	_name = 'commercial.vendor.documents.upload'
	_description = 'Commercial Contract Document'
	
	commercial_vendor_id = fields.Many2one('res.partner', 'Vendor')
	relationship = fields.Selection([
		('candidate', 'Candidate'),
	], 'Relationship')
	person = fields.Many2one('res.partner', 'Name')
	document_name = fields.Char('Document_name', default='Commercial Agreement')
	document = fields.Selection([
		('word_file', 'Word File'),
		('signed_edari_countersigned', 'Signed (Edari) Countersigned'),
	], string='Document')
	contract_date = fields.Date('Contract Date')
	charge_rate = fields.Float('Charge Rate')
	job_title = fields.Char('Job Title')
	client_name = fields.Char('Client Name')
	client_contract = fields.Char('Client Contact')
	site_location = fields.Selection([('dubai', 'Dubai'), ('abu_dhabi', 'Abu Dhabi')], string='Site Location')
	start_date = fields.Date('Start Date')
	end_date = fields.Date('End Date')
	duration = fields.Selection([
		('3', '3 Months'),
		('6', '6 Months'),
		('12', '12 Months'),
		('18', '18 Months'),
		('24', '24 Months'),
	], string='Duration')
	probation_period = fields.Selection([
		('3', '3 Months'),
		('6', '6 Months'),
	], string='Probation Period')
	document_count = fields.Integer('Document Count', compute="compute_document_count")
	last_upload = fields.Datetime('Last Upload', compute="compute_last_upload_date")
	document_ids = fields.One2many('ir.attachment', 'ag_vendor_document_id', string="Documents")
	
	def compute_document_count(self):
		for r in self:
			r.document_count = len(r.document_ids)
	
	def compute_last_upload_date(self):
		for r in self:
			for d in r.document_ids:
				r.last_upload = d.create_date
				break
	
	
class IrAttachment(models.Model):
	_inherit = 'ir.attachment'

	p_vendor_document_id = fields.Many2one('passport.vendor.documents.upload')
	e_vendor_document_id = fields.Many2one('emirates.vendor.documents.upload')
	edu_vendor_document_id = fields.Many2one('edu.vendor.documents.upload')
	insur_vendor_document_id = fields.Many2one('insur.vendor.documents.upload')
	visa_vendor_document_id = fields.Many2one('visa.vendor.documents.upload')
	vp_vendor_document_id = fields.Many2one('vp.vendor.documents.upload')
	ag_vendor_document_id = fields.Many2one('ag.vendor.documents.upload')
	cv_vendor_document_id = fields.Many2one('cv.document.upload')
