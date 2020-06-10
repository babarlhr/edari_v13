# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class DocumentTree(models.Model):
	_name='document.tree'
	_rec_name = 'name'


	document_type = fields.Many2one('document.tree.type',string = "Document")
	name = fields.Char()
	document_number = fields.Char(string="Document Number")
	issue_date = fields.Date(string="Issue Date")
	expiry_date = fields.Date(string="Expiry Date")
	issued_by = fields.Char(string="Issued By")
	place_of_issue = fields.Many2one('place.of.issue',string="Place of Issue")
	country_of_issue = fields.Many2one('res.country', string="Country of Issue")
	upload_doc = fields.Binary(string="Upload Doc")
	doc_count = fields.Integer(string="DOC Count")

	partner_link = fields.Many2one('res.partner')


class DocumentTreeType(models.Model):
	_name='document.tree.type'
	_rec_name = 'name'

	name = fields.Char(string = "Name")


class PlaceofIssue(models.Model):
	_name='place.of.issue'
	_rec_name = 'name'

	name = fields.Char(string = "Name")
	
