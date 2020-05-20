#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
# 
#    from num2words import num2words
#    import base64
#    import re
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
import datetime
from datetime import date, datetime, timedelta
from datetime import date
import time
import calendar
from datetime import time
from dateutil.relativedelta import relativedelta
import datetime as dt



class edari_payslip_report(models.AbstractModel):
    _name = 'report.edari_payslip_report.edari_payslip_report_report'
    _description = "Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        record = self.env['hr.payslip'].browse(docids)

        company = self.env['res.company'].search([('id','=',1)])

        category_list = []
        for x in record:
            for y in x.line_ids:
                if y.category_id not in category_list:
                    category_list.append(y.category_id)


        earning_list = []
        deduction_list = []
        net_sal = 0
        for x in record:
            for y in x.line_ids:
                if y.salary_rule_id.appears_on_payslip:        
                    if y.category_id.name == 'Deduction' and y.category_id.name != 'Net':
                        deduction_list.append(y)
                    if y.category_id.name != 'Deduction' and y.category_id.name != 'Net':
                        earning_list.append(y)
                    if y.category_id.name == 'Net':
                        net_sal = net_sal + y.amount

        # def get_arabic_ear(code):
        #     rule = self.env['hr.salary.rule'].search([('code','=',code)])

            # return rule.arabic_name
            
        # def get_arabic_ded(code):
        #     rule = self.env['hr.salary.rule'].search([('code','=',code)])

        #     return rule.arabic_name


        oldformat_from = str(record.date_from)
        datetimeobject_from = datetime.strptime(oldformat_from,'%Y-%m-%d')
        newformat_from = datetimeobject_from.strftime('%m/%d/%Y')
        oldformat_to = str(record.date_to)
        datetimeobject_to = datetime.strptime(oldformat_to,'%Y-%m-%d')
        newformat_to = datetimeobject_to.strftime('%m/%d/%Y')
        # oldformat_join = str(record.employee_id.join_date)
        # datetimeobject_join = datetime.strptime(oldformat_join,'%Y-%m-%d')
        # newformat_join = datetimeobject_join.strftime('%m/%d/%Y')

        return {
            'doc_ids': docids,
            'doc_model':'hr.payslip',
            'data': data,
            'docs': record,
            'company': company,
            'deduction_list': deduction_list,
            'earning_list': earning_list,
            'net_sal': net_sal,
            # 'get_arabic_ear': get_arabic_ear,
            # 'get_arabic_ded': get_arabic_ded,
            'newformat_from': newformat_from,
            'newformat_to': newformat_to,
            # 'newformat_join': newformat_join,
        }


# class hr_salary_rule_ext(models.Model):
#     _inherit = 'hr.salary.rule'

#     arabic_name = fields.Char(string="Arabic Name")    
