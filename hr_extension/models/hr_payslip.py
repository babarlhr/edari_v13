# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError
from dateutil.relativedelta import *

		
class HRPayslipExt(models.Model):
	_inherit = 'hr.payslip'

	def action_payslip_done(self):

		res = super(HRPayslipExt, self).action_payslip_done()

		if self.move_id:
			if not self.move_id.state == 'cancel':
				if self.move_id.state == 'posted':
					self.move_id.button_draft()
				for x in self.move_id.line_ids:
					x.partner_id = self.employee_id.partner_id.id

		return res

	

		




		
