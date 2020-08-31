# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta,datetime,date
from odoo.exceptions import Warning, ValidationError, UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange
import datetime as dt
import calendar
# import pandas as pd



class AccountInvoiceSend_ext(models.TransientModel):
    _inherit='account.invoice.send'


    def UpdateTemplate(self):

        so_type = ""
        count = 0
        for inv in self.invoice_ids:
            if count == 0:
                so_type = inv.sale_order_id.so_type

            if so_type != inv.sale_order_id.so_type:
                raise ValidationError("You are allowed to send only one type of invoices either Cost Card or Normal at a time")

            count = count + 1

        if (so_type) == 'cost_card':
            find_template = self.env['mail.template'].sudo().search([('model','=','account.move'),('so_type','=','cost_card')])
            if find_template:
                for temp in find_template:
                    if temp.so_type == so_type:
                        self.template_id = temp.id
                        return temp.id
        return False

    @api.model
    def create(self, vals):
      new_record = super(AccountInvoiceSend_ext, self).create(vals)
      new_record.UpdateTemplate()

      return new_record

    @api.onchange('is_email')
    def onchange_is_email(self):
        invoice_template = self.UpdateTemplate()
        if invoice_template == False:
            invoice_template = self.template_id.id
        if self.is_email:
            if not self.composer_id:
                res_ids = self._context.get('active_ids')
                self.composer_id = self.env['mail.compose.message'].create({
                    'composition_mode': 'comment' if len(res_ids) == 1 else 'mass_mail',
                    'template_id': invoice_template
                })
            self.composer_id.template_id = invoice_template
            self.composer_id.onchange_template_id_wrapper()


class MailTemplate_ext(models.Model):
    _inherit='mail.template'

    so_type = fields.Selection([
        ('cost_card','Cost Card'),
        ('sale_order','Sale Order'),
        ], string='SO Type')







