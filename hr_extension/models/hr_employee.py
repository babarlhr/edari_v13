# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class HrEmployeeExtension(models.Model):
	_inherit = 'hr.employee'

	employee_code = fields.Char("Employee Code")



