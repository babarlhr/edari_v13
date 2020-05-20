# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class DocumentTree(models.Model):
	_name='document.tree'
	_rec_name = 'name'


	name = fields.Char(string="Name")
	document_number = fields.Char(string="Document Number")
	issue_date = fields.Date(string="Issue Date")
	expiry_date = fields.Date(string="Expiry Date")
	issued_by = fields.Char(string="Expiry Date")
	place_of_issue = fields.Char(string="Place of Issue")
	country_of_issue = fields.Many2one('res.country', string="Country of Issue")
	upload_doc = fields.Binary(string="Upload Doc")
	doc_count = fields.Integer(string="DOC Count")

	partner_link = fields.Many2one('res.partner')
	
