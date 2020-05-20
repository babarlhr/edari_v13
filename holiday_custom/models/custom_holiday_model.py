# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError


class CustomHoliday(models.Model):
	_name = 'custom.holiday'
	_rec_name = 'year'
	_description = "This is custom holiday module"

	# no_of_days = fields.Integer(string="No of Days", compute='_calculate_days', store=True)
	no_of_days = fields.Integer(string="No of Days")
	state = fields.Selection([
        ('draft','Draft'),
        ('approved','Approved'),
        ],default='draft')

	holidays_tree = fields.One2many('custom.holiday.tree', 'tree_link')


	def set_to_draft(self):
		self.state = 'draft'
		print(self.year)
		print(type(self.year))

	def set_to_approved(self):
		self.state = 'approved'
		print(self.year)
		print(type(self.year))

	def year_selection(self):
	    year = 2000 # replace 2000 with your a start year
	    year_list = []
	    while year != 2050: # replace 2030 with your end year
	        year_list.append((str(year), str(year)))
	        year += 1
	    return year_list

	year = fields.Selection(
	    year_selection,
	    string="Year",
	    default="2019", # as a default value it would be 2019
	)




	# @api.depends('holidays_tree')
	# def _calculate_days(self):
	# 	for x in self:
	# 		if x.holidays_tree:
	# 			x.no_of_days = len(x.holidays_tree)


	def write(self, vals):
		if 'holidays_tree' in vals:
			vals['no_of_days'] = len(vals['holidays_tree'])
		rec = super(CustomHoliday, self).write(vals)

		return rec

class CustomHolidayTree(models.Model):
	_name = 'custom.holiday.tree'
	_rec_name = 'date'
	_description = "Tree Custom Holiday"



	date = fields.Date(string="Date")
	day = fields.Char(string="Day", compute='get_day', store=True)
	description = fields.Char(string="Description")
	

	tree_link = fields.Many2one('custom.holiday')


	@api.depends('date')
	def get_day(self):
		for x in self:
			if x.date:
				if x.date.weekday() == 0:
					x.day = "Monday"
				if x.date.weekday() == 1:
					x.day = "Tuesday"
				if x.date.weekday() == 2:
					x.day = "Wednesday"
				if x.date.weekday() == 3:
					x.day = "Thursday"
				if x.date.weekday() == 4:
					x.day = "Friday"
				if x.date.weekday() == 5:
					x.day = "Satuarday"
				if x.date.weekday() == 6:
					x.day = "Sunday"
			else:
				x.day = False


	