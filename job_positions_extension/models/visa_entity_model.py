# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class VisaEntity(models.Model):
	_name ='visa.entity'
	_rec_name = 'name'

	name = fields.Char(string="Name")
