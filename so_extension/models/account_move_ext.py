# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError

from datetime import datetime
from dateutil.relativedelta import relativedelta


class AccMoveExt(models.Model):
	_inherit='account.move'

	sale_order_id = fields.Many2one('sale.order',string="Sale Order")
	employee = fields.Many2one('hr.employee', string="Employee")
	