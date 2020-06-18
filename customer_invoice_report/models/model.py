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
from odoo import api, models

class customer_invoice_report(models.AbstractModel):
    _name = 'report.customer_invoice_report.customer_invoice'
    _description = "Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        record = self.env['account.move'].browse(docids)

        company = self.env['res.company'].search([('id','=',1)])
        contacts = {}
        
        inv_attention = ""
        inv_requestor = ""
        inv_buyer = ""
        inv_attention = record.partner_id.inv_attention
        for x in record.partner_id.child_ids:
            if x.function_contact == 'inv_requestor':
                inv_requestor = x.name
            if x.function_contact == 'inv_buyer':
                inv_buyer = x.name


        # getting tax rate
        vat_rate = []
        vat_amount = 0
        label = ""
        for x in record.invoice_line_ids:
            for y in x.tax_ids:
                if str(y.amount) not in vat_rate:
                    if len(vat_rate) == 0:
                        vat_amount = int(y.amount)
                    else:
                        vat_amount = 0

                    vat_rate.append(str(y.amount))


        bank_name = ""
        iban = ""
        swift = ""
        bank_name = company.partner_id.bank_ids[0].bank_id.name
        swift = company.partner_id.bank_ids[0].bank_id.swift
        iban = company.partner_id.bank_ids[0].acc_number

        contract = self.env['hr.contract'].search([('employee_id','=',record.employee.id)])

        line_man = contract.line_manager_client.name




        return {
            'doc_ids': docids,
            'doc_model':'account.move',
            'data': data,
            'inv_attention': inv_attention,
            'inv_requestor': inv_requestor,
            'inv_buyer': inv_buyer,
            'vat_amount': vat_amount,
            'bank_name': bank_name,
            'iban': iban,
            'swift': swift,
            'line_man': line_man,
            'docs': record,
            'company': company,
        }


