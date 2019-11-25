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

    visa_category = fields.Selection([
        ('gems_emp', 'GEMS Employees'),
        ('sraco_emp', 'SRACO Employees'),
        ('saed_emp', 'SAED Employees'),
        ('jeban_emp', 'Jehan Employees'),
        ('massader_company', 'Massader Company'),
        ('saudi', 'Saudi'),
    ], string="Visa Category")

    @api.model
    def create(self, vals):
        res = super(Employee, self).create(vals)
        employees = self.env['hr.employee'].search([
            ('name', '=', res.with_context(lang='eng_US').name),
            ('iqama_no', '=', res.iqama_no),
        ])
        if len(employees) > 1:
            raise UserError('Employee with name {0} and Iqama No {1} already exist. You can not create duplicate records'.format(res.name, res.iqama_no))
        return res

    def write(self, vals):
        res = super(Employee, self).write(vals)
        employees = self.env['hr.employee'].search([
            ('name', '=', self.with_context(lang='eng_US').name),
            ('iqama_no', '=', self.iqama_no),
        ])
        if len(employees) > 1:
            raise UserError(
                'Employee with name {0} and Iqama No {1} already exist. You can not create duplicate records'.format(
                    self.name, self.iqama_no))
        return res
