#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
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
# from odoo import models, fields, api

# class CostCard(models.AbstractModel):
#     _name = 'report.cost_card_report.cost_card'

#     @api.model
#     def render_html(self,docids, data=None):
#         report_obj = self.env['ir.actions.report']
#         report = report_obj._get_report_from_name('cost_card_report.cost_card')
#         records = self.env['sale.order'].browse(docids)


#         company = self.env['res.company'].search([])

#         docargs = {
#             'doc_ids': docids,
#             'doc_model': 'sale.order',
#             'docs': records,
#             'data': data,
#             'company': company,
#             }

#         return report_obj.render('cost_card_report.cost_card', docargs)

from odoo import api, models

class CostCard(models.AbstractModel):
    _name = 'report.cost_card_report.cost_card'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('cost_card_report.cost_card')
        docargs = {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': self,
        }
        return docargs