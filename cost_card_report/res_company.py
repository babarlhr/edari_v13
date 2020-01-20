# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class sale_order(models.Model):
    _inherit = 'sale.order'

    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env.ref('cost_card_report.cost_card').report_action(self)
