# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrderTags(models.Model):
    _name = 'purchase.order.tag'
    _rec_name = 'name'
    _order = 'id desc'
     
    name = fields.Char('Name')