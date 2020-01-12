# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class PartnerExtension(models.Model):
	_inherit='res.partner'

	trade_license_no = fields.Char("Trade License No")
	