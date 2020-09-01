from odoo import models, fields, api
from odoo.exceptions import UserError




class IrAttachment(models.Model):
    _inherit = "ir.attachment"
    
    employee_ext_id = fields.Many2one('hr.employee', string="Employee")
    doc_type = fields.Selection([
        ('passport', 'Passport'),
        ('visa', 'Visa'),
        ('iqama', 'Iqama'),
        ('driver_licence', 'Driver Licence'),
        ('tenancy_agreement', 'Tenancy Agreement'),
        ('vehicle_reg', 'Vehicle Registeration'),
        ('med_isur_policy', 'Medical Insurance Policy'),
        ('med_insur_card', 'Medical Insrance Card'),
    ])


class EmployeeEvent(models.Model):
    _name = 'employee.event'
    
    employee_ids = fields.Many2one('hr.employee', string="Event", required=True, ondelete='cascade', index=True,
                                   copy=False)
    event_date = fields.Date('Event Date')
    event_desc = fields.Char('Event Desc')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', attachment=True)


class EmployeeAccomodationHistory(models.Model):
    _name = 'employee.accomodation.history'
    
    employee_acc_ids = fields.Many2one('hr.employee', string="Event", required=True, ondelete='cascade', index=True,
                                       copy=False)
    event_date = fields.Date('Event Date')
    event_desc = fields.Char('Event Desc')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', attachment=True)


class EmployeeTransportationHistory(models.Model):
    _name = 'employee.transportation.history'
    
    employee_tran_ids = fields.Many2one('hr.employee', string="Event", required=True, ondelete='cascade', index=True,
                                        copy=False)
    event_date = fields.Date('Event Date')
    event_desc = fields.Char('Event Desc')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', attachment=True)


class EmployeeAccidentHistory(models.Model):
    _name = 'employee.accident.history'
    
    employee_accident_ids = fields.Many2one('hr.employee', string="Event", required=True, ondelete='cascade',
                                            index=True, copy=False)
    event_date = fields.Date('Event Date')
    event_desc = fields.Char('Event Desc')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', attachment=True)


class EmployeeVacationHistory(models.Model):
    _name = 'employee.vacation.history'
    
    employee_vac_ids = fields.Many2one('hr.employee', string="Event", required=True, ondelete='cascade', index=True,
                                       copy=False)
    event_date = fields.Date('Event Date')
    event_desc = fields.Char('Event Desc')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', attachment=True)


class EmployeeTrainingHistory(models.Model):
    _name = 'employee.training.history'
    
    employee_train_ids = fields.Many2one('hr.employee', string="Event", required=True, ondelete='cascade', index=True,
                                         copy=False)
    event_date = fields.Date('Event Date')
    event_desc = fields.Char('Event Desc')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', attachment=True)


class EmployeeHSEIncidentHistory(models.Model):
    _name = 'employee.hse.incident.history'
    
    employee_hse_ids = fields.Many2one('hr.employee', string="Event", required=True, ondelete='cascade', index=True,
                                       copy=False)
    event_date = fields.Date('Event Date')
    event_desc = fields.Char('Event Desc')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', attachment=True)


class EmployeeCareerProgress(models.Model):
    _name = 'employee.career.progression'
    
    employee_career_ids = fields.Many2one('hr.employee', string="Event", required=True, ondelete='cascade', index=True,
                                          copy=False)
    event_date = fields.Date('Event Date')
    event_desc = fields.Char('Event Desc')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', attachment=True)


class Employee(models.Model):
    _inherit = "hr.employee"
    
    name = fields.Char(related='resource_id.name', string="Name (EN)", store=True, oldname='name_related')
#     Genaral information group
    join_date = fields.Date('Joining Date')
    private_email = fields.Char(string="Private Email", store=True)
    # related='address_home_id.email', 
    line_manager = fields.Many2one('hr.employee' , 'Line Manager')
    senior_manager = fields.Many2one('hr.employee' , 'Senior Manager')
    contract_signing_date = fields.Date('Contract Signing Date')
    
#     Medical group
    medical_insur = fields.Selection([
                                        ('provided', 'Provided'),
                                        ('not_provided' , 'Not Provided'),
                                    ], 'Medical Insurance')
    medical_insur_no = fields.Char('Medical Insurance No:')
    MI_carrier = fields.Char('Carrier')
    MI_poloicy_type = fields.Char('Policy Type')
    medical_history = fields.Text('Medical History')
    blood_type = fields.Char('Blood Type')
    next_to_kin = fields.Char('Next to Kin')
    
#     General tab
    local_address = fields.Char('Local Address')
    personal_mob = fields.Char('Personal Mobile')
    personal_email = fields.Char('Personal Email')
    language_spoken = fields.Many2one('res.lang', 'Language Spoken')
    name_ar = fields.Char('Name (AR)')
    job_location = fields.Char('Job Location')
    designation = fields.Char('Designation')
    company_identification = fields.Char('Company ID')
    home_company_address = fields.Char('Home Company Address')
    passport_expiry = fields.Date('Passport Expiry')
    name_in_passport = fields.Char('Name in passport', translate=True)
    visa_type = fields.Char('Visa Type')
    driver_licence_no = fields.Char('Driver Licence No')
    driver_licence_class = fields.Char('Driver Licence Classification')
    vehicle_plate_no = fields.Char('Vehicle Plate No:')
    iqama_no = fields.Char('Iqama Number', copy=False)
    iqama_name = fields.Char('Name in Iqama')
    iqama_expiry = fields.Date('Iqama Expiry')
    iqama_profession = fields.Char('Iqama Profession(EN)')
    iqama_profession_ar = fields.Char('Iqama Profession(AR)')
    dob_hijri = fields.Char('Date Of Birth (Hijri)')
    
#     Medical Records
    med_ins_policy_no = fields.Char('Medical Insurance Policy No')
    primary_hosp_home = fields.Char("Primary Hospital(Home)")
    primary_hosp_local = fields.Char('Primary Hospital(Local)')
    primary_care_physician_home = fields.Char('Primary Care Physician(Home)')
    primary_care_physician_local = fields.Char('Primary Care Physician(Local)')
    contact_details_home = fields.Char('Contact Details(Home)')
    contact_details_local = fields.Char('Contact Details(Local)')
    policy_exipry = fields.Date('Policy Expiry Date')
    carrier = fields.Char('Carrier')
    class_c = fields.Char("Class")
    
#     IT
    computer_tag = fields.Char('Computer Tag')
    compute_id = fields.Many2one('account.asset', string="Computer")
    phone_tag = fields.Char('Phone Tag')
    mobile_id = fields.Many2many('account.asset', string="Mobile")
    vehicle_id = fields.Many2one('account.asset', string="Vehicle")
    imie_tag = fields.Char('IMIE Tag')
    
    docs_ids = fields.One2many('ir.attachment', 'employee_ext_id', string="Docs to Upload")

    emp_event_ids = fields.One2many('employee.event', 'employee_ids', string="Event")
    emp_event_accomodation_ids = fields.One2many('employee.accomodation.history', 'employee_acc_ids', string="Accomodation History")
    emp_event_transportation_ids = fields.One2many('employee.transportation.history', 'employee_tran_ids', string="Transportation History")
    emp_event_accident_ids = fields.One2many('employee.accident.history', 'employee_accident_ids', string="Accident History")
    emp_event_vacation_ids = fields.One2many('employee.vacation.history', 'employee_vac_ids', string="Vacation History")
    emp_event_training_ids = fields.One2many('employee.training.history', 'employee_train_ids', string="Training History")
    emp_event_hse_incident_ids = fields.One2many('employee.hse.incident.history', 'employee_hse_ids', string="HSE Incident History")
    emp_event_career_ids = fields.One2many('employee.career.progression', 'employee_career_ids', string="Career Progression")
    dependent_tree = fields.One2many('employee.dependent.tree', 'tree_link')

    visa_category = fields.Selection([
        ('gems_emp', 'GEMS Employees'),
        ('sraco_emp', 'SRACO Employees'),
        ('saed_emp', 'SAED Employees'),
        ('jeban_emp', 'Jehan Employees'),
        ('massader_company', 'Massader Company'),
        ('saudi', 'Saudi'),
    ], string="Visa Category")



    # New fields by jaffar raza
    allow_multiple_loans = fields.Boolean(string="Allow Multiple Loans")
    loan_defaulter = fields.Boolean(string="Loan Defaulter")
    education = fields.Many2one('hr.education', string="Education")
    cv = fields.Binary(string="CV")
    cv_name = fields.Char(string="CV")
    contact_no = fields.Char(string="Contact No")
    client_email = fields.Char(string="Client Email")
    sick_leaves = fields.Char(string="Sick Leaves")
    bank_name = fields.Char(string="Bank Name")
    branch_name = fields.Char(string="Branch Name")
    beneficiary_name = fields.Char(string="Beneficiary Name")
    account_no = fields.Char(string="Account No")
    iban = fields.Char(string="IBAN")
    swift_routing_no = fields.Char(string="Swift or Routing No")
    other_key_number = fields.Char(string="Other Key Number")
    education_tree = fields.One2many('hr.education.tree', 'tree_link')
    address = fields.Char('Address')
    


    uae_visa_held = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="UAE Visa Held")
    prob_period = fields.Selection([
        ('3', '3 Months'),
        ('6', '6 Months'),
    ], string="Probation Period")
    notice_period = fields.Selection([
        ('1', '1 Months'),
        ('3', '3 Months'),
    ], string="Notice Period")
    work_days = fields.Selection([
        ('22', '22 Days'),
    ], string="Working Days")
    visa_entity = fields.Selection([
        ('levo', 'Levo'),
        ('edari', 'Edari'),
    ], string="Visa Entity")

    child_depend = fields.Selection([
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
    ], string="Children (Dependent)")


    # education tabs fields
    # level_of_education = fields.Selection([
    #     ('high_school', 'High School'),
    #     ('bachelors', 'Bachelors'),
    #     ('masters', 'Masters'),
    #     ('phd', 'Phd'),
    # ], string="Level of Education")
    # university = fields.Char(string="University")
    # country = fields.Many2one('res.country', string="Country")

    # certificate_2 = fields.Selection([
    #     ('bachelors', 'Bachelors'),
    #     ('masters', 'Masters'),
    #     ('other', 'Other'),
    # ], string="Certificate Level")
    # study_field_2 = fields.Char(string="Field of Study")
    # study_school_2 = fields.Char(string="School")
    # level_of_education_2 = fields.Selection([
    #     ('high_school', 'High School'),
    #     ('bachelors', 'Bachelors'),
    #     ('masters', 'Masters'),
    #     ('phd', 'Phd'),
    # ], string="Level of Education")
    # university_2 = fields.Char(string="University")
    # country_2 = fields.Many2one('res.country', string="Country")

    # add_education = fields.Boolean(string='Add Education')



    @api.onchange('add_education')
    def emplty_second_education_fields(self):
        if not self.add_education:
            self.certificate_2 = None
            self.study_field_2 = None
            self.study_school_2 = None
            self.level_of_education_2 = None
            self.university_2 = None
            self.country_2 = None


    @api.model
    def create(self, vals):
        res = super(Employee, self).create(vals)
        employees = self.env['hr.employee'].search([
            ('name', '=', res.with_context(lang='eng_US').name),
            ('iqama_no', '=', res.iqama_no),
            ('id', '!=', res.id),
        ])
        if len(employees) > 1:
            raise UserError('Employee with name {0} and Iqama No {1} already exist. You can not create duplicate records'.format(res.name, res.iqama_no))
        return res

    def write(self, vals):
        res = super(Employee, self).write(vals)
        employees = self.env['hr.employee'].search([
            ('name', '=', self.with_context(lang='eng_US').name),
            ('iqama_no', '=', self.iqama_no),
            ('id', '!=', self.id),
        ])
        if len(employees) > 1:
            raise UserError(
                'Employee with name {0} and Iqama No {1} already exist. You can not create duplicate records'.format(
                    self.name, self.iqama_no))
        return res


class HrEducationTree(models.Model):
    _name = 'hr.education.tree'
    _rec_name = 'certificate_level'

    certificate_level = fields.Many2one('certificate.level', string='Certificate Level')
    field_of_study = fields.Char(string='Field of Study')
    institute_id = fields.Many2one('education.institute', string='Institute')
    country_id = fields.Many2one('res.country', string='Country')
    year_of_graduation = fields.Char(string = "Year of Graduation")



    uae_attested = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="UAE Attested")

    mofa_attestation = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string="MOFA Attestation")
    upload_doc = fields.Many2many('ir.attachment', string='Upload Doc', attachment=True)
    doc_count = fields.Integer(string = "DOC Count")

    tree_link = fields.Many2one('hr.employee')


class CertificateLevel(models.Model):
    _name = 'certificate.level'
    _rec_name = 'name'

    name = fields.Char(string='Name')


class EducationInstitute(models.Model):
    _name = 'education.institute'
    _rec_name = 'name'

    name = fields.Char(string='Name')


class HeEducation(models.Model):
    _name = 'hr.education'
    _rec_name = 'name'

    name = fields.Char(string="Name")


class DependentTree(models.Model):
    _name = 'employee.dependent.tree'
    _rec_name = 'display_name'

    display_name = fields.Char(string="Display Name")
    name_in_passport = fields.Char(string="Name in Passport")
    country_id = fields.Many2one('res.country', string="Nationality (country)")
    birthday = fields.Date(string="Date of Birth")
    relationship = fields.Many2one('employee.dependent.relation')

    # relation = fields.Selection([
    #     ('spouse', 'Spouse'),
    #     ('child1', 'Child 1'),
    #     ('child2', 'Child 2'),
    #     ('child3', 'Child 3'),
    #     ('child4', 'Child 4'),
    #     ('child5', 'Child 5'),
    #     ('child6', 'Child 6'),
    #     ('child7', 'Child 7'),
    #     ('parent1', 'Parent 1'),
    #     ('parent2', 'Parent 2'),
    # ], string="Relationship")

    tree_link = fields.Many2one('hr.employee')

class DependentTreeRelation(models.Model):
    _name = 'employee.dependent.relation'

    name = fields.Char()
