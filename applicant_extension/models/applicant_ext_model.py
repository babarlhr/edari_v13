# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class HrApplicantExt(models.Model):
	_inherit = 'hr.applicant'

	cost_card = fields.Many2one('sale.order', string="Cost Card")
	contract = fields.Many2one('hr.contract', string="Contract")
	payroll_structure = fields.Many2one('hr.payroll.structure.type', string="Salary Structure")
	approve_stage = fields.Boolean(string="Approve Boolean")

	# @api.depends('cost_card')
	# def _compute_salary(self):
	# 	print ("DDDDDDDDDDDDDDDDDDDDDDDDDDd")
	# 	if self.cost_card:
	# 		self.salary_expected = self.cost_card.per_month_gross_salary
			
	# salary_expected = fields.Float(string="Expected Salary", compute='_compute_salary', store=True)

	# Adding a new value in selection field
	# stage_id = fields.Selection(selection_add=[('approved','Approved')])



	# def create_so(self):
	#   # cost_card = self.cost_card.create({
	#   cost_card = self.env['sale.order'].create({
	#       'candidate_name':self.partner_name,
	#       'applicant':self.id,
	#       'contract_start_date':self.availability,
	#       'per_month_gross_salary':self.salary_expected,
	#       'job_pos':self.job_id.id,
	#       'template':self.job_id.template.id,
	#       'partner_id':self.job_id.customer.id,
	#       'no_of_months':int(self.job_id.contract_length),
	#       })
	#   self.cost_card = cost_card.id
	#   self.cost_card.get_contract_end_date()



	def create_so(self):
		rec = self.env['sale.order'].search([('applicant','=',self.id)]).ids
		domain = [('id','in',rec)]
		# view_id_tree = self.env['ir.ui.view'].search([('name','=',"semester.tree")])department_id=self.department_id.id)
		return {
		'type': 'ir.actions.act_window',
		 'name': ('Job'),
		 'res_model': 'sale.order',
		 'view_type': 'form',
		 'view_mode': 'tree,form',
		 # 'views': [(view_id_tree[0].id, 'tree'),(False,'form')],
		 'context': {
			'default_candidate_name':self.partner_name,
			# 'partner_id':self.job_id.customer.id,
			'default_applicant':self.id,
			'default_contract':self.contract.id,
			'default_contract_start_date':self.availability,
			'default_per_month_gross_salary':self.salary_expected,
			'default_job_pos':self.job_id.id,
			'default_template':self.job_id.template.id,
			'default_partner_id':self.job_id.customer.id,
			'default_no_of_months':int(self.job_id.contract_length),
		 },
		 'view_id ref=" sale.view_quotation_tree_with_onboarding"': '',
		 'target': 'current',
		 'domain': domain,
		}


	def approve_btn(self):
		recs = self.env['hr.recruitment.stage'].search([('name','=','Approved')])
		self.stage_id = recs.id
		self._get_approve_stage()

	@api.onchange('stage_id')
	def _get_approve_stage(self):
		for x in self:
			if x.stage_id.name == 'Approved':
				x.approve_stage = True
			else:
				x.approve_stage = False

	def create_contract(self):
		print ('Create Contract')
		contract_rec = self.env['hr.contract'].create({
			'name':self.name,
			'department_id':self.department_id.id,
			'job_id':self.job_id.id,
			'employee_id':self.emp_id.id,
			'wage':self.salary_expected,
			'structure_type_id':self.payroll_structure.id,
			})

		self.contract = contract_rec.id









