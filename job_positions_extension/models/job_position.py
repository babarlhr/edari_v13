# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class JobsExtension(models.Model):
	_inherit='hr.job'

	customer = fields.Many2one('res.partner')
	