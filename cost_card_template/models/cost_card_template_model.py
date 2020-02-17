# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class CostCardTemplate(models.Model):
	_name = 'costcard.template'
	_rec_name = 'template_name'
	_description = "Model for Template"

	template_name = fields.Char(string="Template Name")
	job_position = fields.Many2one('hr.job', string="Job Position")
	customer = fields.Many2one('res.partner', string="Customer")
	
	active = fields.Boolean(string="Active", default=True)

	template_tree = fields.One2many('costcard.template.tree', 'tree_link')


class CostCardTemplateTree(models.Model):
	_name = 'costcard.template.tree'
	_rec_name = 'service_name'
	_description = "Tree Model for Template"



	handle = fields.Char(string="Handle")
	service_name = fields.Many2one('product.product', string="Service Name")
	service_category = fields.Many2one('product.category', string="Service Category")
	chargable = fields.Boolean(string="Chargable")
	account_head = fields.Many2one('account.account', string="Account Head")
	sequence = fields.Char(string="Sequence", readonly=True)
	code = fields.Char(string="Code")
	computation_formula = fields.Text(string="Computation Formula")
	computation_qty = fields.Text(string="Computation Qty")
	# fixed = fields.Boolean(string="Fixed")
	based_on_wd = fields.Boolean(string="Based on WD")

	payment_type = fields.Selection([
        ('upfront','Upfront'),
        ('end','End'),
        ('interval','Interval')
        ], string='Payment Type', default='upfront')
	costcard_type = fields.Selection([
        ('fixed','Fixed'),
        ('manual','Manual'),
        ('calculation','Calculation'),
        ], string='Type', default='fixed')

	tree_link = fields.Many2one('costcard.template')

	@api.onchange('service_name')
	def get_service_categ(self):
		if self.service_name:
			self.service_category = self.service_name.categ_id.id
		else:
			self.service_category = None

	# @api.model
	# def create(self, vals):
	# 	# vals['sequence'] = self.env['ir.sequence'].next_by_code('cost.card.seq')
	# 	new_record = super(CostCardTemplateTree, self).create(vals)
	# 	new_record.check_if_space()
	# 	new_record.check_if_import()
	# 	new_record.check_specific_code_strings()
	# 	return new_record

	# # @api.multi
	# def write(self, vals):
	# 	rec = super(CostCardTemplateTree, self).write(vals)
	# 	self.check_if_space()
	# 	self.check_if_import()
	# 	self.check_specific_code_strings()
	# 	return True


	# def check_if_space(self):
	# 	if self.computation_formula:
	# 		if ' ' in self.computation_formula:
	# 			raise ValidationError("No blank spaces allowed in computation formula.")

	# def check_specific_code_strings(self):
	# 	if self.code in ['salary', 'compute_result']:
	# 		raise ValidationError("You cannot use '%s' keyword as code." % (self.code))



	# def check_if_import(self):
	# 	if self.computation_formula:
	# 		if 'import' in self.computation_formula:
	# 			raise ValidationError("No 'import' key word allowed in computation formula.")
