# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class HrContractExtension(models.Model):
	_inherit = 'hr.contract'

	contract_length = fields.Char("Contract Length")
	