# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError, UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import datetime as dt
# import pandas as pd


class HrContractExt(models.Model):
	_inherit='hr.contract'


	salary_batch_interval = fields.Selection([
        ('monthly','Monthly'),
        ('fortnightly','Fortnightly'),
        ('weekly','Weekly'),
        ('four_weekly','4 Weekly'),
        ], string='Salary Batch Interval', default='monthly')


class HrPayslipRunExt(models.Model):
	_inherit='hr.payslip.run'


	salary_batch_interval = fields.Selection([
        ('monthly','Monthly'),
        ('fortnightly','Fortnightly'),
        ('weekly','Weekly'),
        ('four_weekly','4 Weekly'),
        ], string='Salary Batch Interval', default='monthly')

	def days_add_func(self, start_date, end_date, days_to_add):
		start = str(start_date)
		end = str(end_date)
		days_in_month = self.number_of_days_in_month(start_date.year, start_date.month)

		temp = int(start[-2:])+days_to_add
		if temp <= days_in_month:
			date_end = start_date + relativedelta(days=days_to_add)
		else:
			remain = (days_to_add-(days_in_month - int(start[-2:])))
			start_temp = start_date.replace(day=1)

			if start_temp.month == 12:
				start_temp = start_temp + relativedelta(years = 1)

			start_temp = start_temp + relativedelta(months=1)
			date_end = start_temp + relativedelta(days=remain)

		return date_end

	@api.onchange('salary_batch_interval', 'date_start')
	def get_end_date(self):
		remain = 0
		days_in_month = 0
		if self.salary_batch_interval == 'monthly':
			if self.date_start.month == 12:
				temp = self.date_start + relativedelta(months=1)
				self.date_end = temp + relativedelta(years=1)
			else:
				self.date_end = self.date_start + relativedelta(months=1)

		if self.salary_batch_interval == 'fortnightly':
			self.date_end = self.days_add_func(self.date_start, self.date_end, 14)
			# start = str(self.date_start)
			# end = str(self.date_end)
			# days_in_month = self.number_of_days_in_month(self.date_start.year, self.date_start.month)

			# temp = int(start[-2:])+14
			# if temp <= days_in_month:
			# 	self.date_end = self.date_start + relativedelta(days=14)
			# else:
			# 	remain = (14-(days_in_month - int(start[-2:])))
			# 	start_temp = self.date_start.replace(day=1)

			# 	if start_temp.month == 12:
			# 		start_temp = start_temp + relativedelta(years = 1)

			# 	start_temp = start_temp + relativedelta(months=1)
			# 	self.date_end = start_temp + relativedelta(days=remain)


		if self.salary_batch_interval == 'weekly':
			self.date_end = self.days_add_func(self.date_start, self.date_end, 7)

			# start = str(self.date_start)
			# end = str(self.date_end)
			# days_in_month = self.number_of_days_in_month(self.date_start.year, self.date_start.month)

			# temp = int(start[-2:])+7
			# if temp <= days_in_month:
			# 	self.date_end = self.date_start + relativedelta(days=7)
			# else:
			# 	print(days_in_month)
			# 	print(start[-2:])
			# 	remain = (7-(days_in_month - int(start[-2:])))
			# 	print (remain)
			# 	print ("XXXXXXXXXXXXXXXXXXXxx")
			# 	start_temp = self.date_start.replace(day=1)

			# 	if start_temp.month == 12:
			# 		start_temp = start_temp + relativedelta(years = 1)
					
			# 	start_temp = start_temp + relativedelta(months=1)
			# 	print (start_temp)
			# 	self.date_end = start_temp + relativedelta(days=remain)


		if self.salary_batch_interval == 'four_weekly':
			self.date_end = self.days_add_func(self.date_start, self.date_end, 28)

			# start = str(self.date_start)
			# end = str(self.date_end)
			# days_in_month = self.number_of_days_in_month(self.date_start.year, self.date_start.month)

			# temp = int(start[-2:])+28
			# if temp <= days_in_month:
			# 	self.date_end = self.date_start + relativedelta(days=28)
			# else:
			# 	remain = (28-(days_in_month - int(start[-2:])))
			# 	start_temp = self.date_start.replace(day=1)

			# 	if start_temp.month == 12:
			# 		start_temp = start_temp + relativedelta(years = 1)
					
			# 	start_temp = start_temp + relativedelta(months=1)
			# 	print (start_temp)
			# 	self.date_end = start_temp + relativedelta(days=remain)




	def number_of_days_in_month(self, year, month):
		return monthrange(year, month)[1]

	def add_days_to_date(self, date):
		temp = str(date)
		days = int(temp[-2:])
		days += 1
		temp = temp[:-2]+str(days)

	def add_month_to_date(self, date):
		temp = str(date)
		month = int(temp[5:7])
		year = int(temp[0:4])
		day = int(temp[8:])
		if month == 12:
			day = 1
			month = 1
			year += 1
			temp = str(year)+"-0"+str(month)+"-0"+str(day)
		else:
			month += 1
			temp = temp[0:5]+str(month)+temp[7:]
		return temp

	def sub_days_to_date(self, date):
		temp = str(date)
		days = int(temp[-2:])
		days -= 1
		temp = temp[:-2]+str(days)

	def sub_month_to_date(self, date):
		temp = str(date)
		day = int(temp[8:])
		month = int(temp[5:7])
		year = int(temp[0:4])
		if month == 1:
			day = self.number_of_days_in_month(int(year), int(month))
			month = 12
			year -=1
			temp = str(year)+"-"+str(month)+"-"+str(day)
		else:
			month -= 1
			temp = temp[0:5]+str(month)+temp[7:]
		return temp

