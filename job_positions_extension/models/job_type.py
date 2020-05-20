# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class JobType(models.Model):
	_name ='job.type'
	_rec_name = 'name'

	name = fields.Char(string="Name")
