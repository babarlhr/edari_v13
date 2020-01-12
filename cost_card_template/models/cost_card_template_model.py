# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class CostCardTemplate(models.Model):
	_name = 'costcard.template'
	_rec_name = 'template_name'

	template_name = fields.Char(string="Template Name")
	job_position = fields.Many2one('hr.job', string="Job Position")
	
	active = fields.Boolean(string="Active", default=True)

	template_tree = fields.One2many('costcard.template.tree', 'tree_link')

class CostCardTemplateTree(models.Model):
	_name = 'costcard.template.tree'
	_rec_name = 'service_name'

	service_name = fields.Many2one('product.product', string="Service Name")
	service_category = fields.Many2one('product.category', string="Service Category")
	chargable = fields.Boolean(string="Chargable")
	account_head = fields.Many2one('account.account', string="Account Head")
	sequence = fields.Char(string="Sequence")
	computation_formula = fields.Text(string="Computation Formula") 

	tree_link = fields.Many2one('costcard.template')

	@api.model
	def create(self, vals):
		vals['sequence'] = self.env['ir.sequence'].next_by_code('cost.card.seq')
		new_record = super(CostCardTemplateTree, self).create(vals)

		return new_record
