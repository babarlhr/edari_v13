# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
import base64
from odoo.addons.purchase.models.purchase import PurchaseOrder


def button_confirm(self):
	for order in self:
		if order.state not in ['draft', 'sent']:
			continue
		order._add_supplier_to_product()
		# Deal with double validation process
		if order.company_id.po_double_validation == 'one_step' \
				or (order.company_id.po_double_validation == 'two_step' \
					and order.amount_total < self.env.user.company_id.currency_id._convert(
					order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
					order.date_order or fields.Date.today())):
			order.button_approve()
		else:
			order.is_app_manager = True
			order.write({'state': 'select_manager'})
	return True


PurchaseOrder.button_confirm = button_confirm


class PurchaseOrderNew(models.Model):
	_inherit = 'purchase.order'

	state = fields.Selection(selection_add=[
		('select_manager', 'Approval Selection'),
		('to approve', 'To Approve'),
		('approval_1', 'Approval 1'),
		('approval_2', 'Approval 2'),
	], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
	is_app_manager = fields.Boolean("Approve manager selection")
	supplier_criteria = fields.Char('Supplier Selection Criteria')
	doc_ids = fields.One2many('ir.attachment', 'purchase_id', 'Attachments')

	comments = fields.Text("Comments")
	approver_1 = fields.Many2one('res.users', inverse="_inverse_approval_by_group", string="Approver 1",
								 track_visibility='onchange')
	approver_2 = fields.Many2one('res.users', inverse="_inverse_approval_by_group", string="Approver 2",
								 track_visibility='onchange')

	approver_1_approved_date = fields.Datetime(string="Approval_1 Approved Date")
	approver_2_approved_date = fields.Datetime(string="Approval_2 Approved Date")

	approver_1_state = fields.Selection([
		('pending', 'Pending'),
		('hold', 'On-Hold'),
		('done', 'Approved'),
		('cancelled', 'Rejected')
	], string="Approver 1 State", default='pending')
	approver_2_state = fields.Selection([
		('pending', 'Pending'),
		('hold', 'On-Hold'),
		('done', 'Approved'),
		('cancelled', 'Rejected')
	], string="Approver 2 State", default='pending')

	is_approver_1 = fields.Boolean(compute='_compute_is_approver')
	is_approver_2 = fields.Boolean(compute='_compute_is_approver')

	approver_1_date = fields.Datetime('Approval 1 date')
	approver_2_date = fields.Datetime('Approval 1 date')
	submission_date = fields.Datetime('Submission Date', copy=False)
	procurment_manager = fields.Many2one('hr.employee', string="Procurment Manager")
	procurment_officer = fields.Many2one('hr.employee', string="Procurment Officer")
	# requesting_operating_unit_id = fields.Many2one('operating.unit', string="Requesting OU")
	description = fields.Text('Description')
	billing_poc_id = fields.Many2one('hr.employee', string='Billing POC')
	billing_poc_email = fields.Char('Billing POC Email')
	billing_poc_phone = fields.Char('Billing POC Phone')
	delivery_poc_id = fields.Many2one('hr.employee', string='Delivery POC')
	special_conditions = fields.Html(string='Special Conditions')
	tags = fields.Many2many('purchase.order.tag', string="Tags")
	partner_bill_to_id = fields.Many2one(
		'res.partner', string='Billing Address',
		readonly=True, required=False,
		states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'select_manager': [('readonly', False)]},
		help="Invoice address for current purchase order.",
		domain=lambda self: [('type', 'in', ['invoice'])],
		# domain=lambda self: [('type','in',['invoice']),('parent_id', '=', self.env.user.company_id.partner_id.id)]
	)

	@api.onchange('billing_poc_id')
	def onchange_billing_poc_id(self):
		for p in self:
			p.billing_poc_email = p.billing_poc_id.work_email
			p.billing_poc_phone = p.billing_poc_id.work_phone

	@api.depends('state')
	def _compute_is_approver(self):
		cid = self.env.uid
		if self.approver_1.id == cid:
			self.is_approver_1 = True
		else:
			self.is_approver_1 = False
		if self.approver_2.id == cid:
			self.is_approver_2 = True
		else:
			self.is_approver_2 = False

	#   Add users to the followers of the activity
	def _inverse_approval_by_group(self):
		for p in self:
			partner_ids = []
			# -- Approver_1
			if p.approver_1:
				partner_ids.append(p.approver_1.partner_id.id)
			# -- Approver_2
			if p.approver_2:
				partner_ids.append(p.approver_2.partner_id.id)
			partner_ids = list(set(partner_ids))
			p.message_subscribe(partner_ids=partner_ids)

	def activity_log(self):
		approval_type = None
		responsible_id = None
		approval_name = None
		if self.state == 'approval_1':
			if self.approver_1:
				responsible_id = self.approver_1
				approval_type = 'Approval_1'
				approval_name = self.approver_1.partner_id
		elif self.state == 'approval_2':
			responsible_id = self.approver_2
			approval_type = 'Approval_2'
			approval_name = self.approver_2.partner_id
		else:
			responsible_id = self.env.user
			approval_name = self.env.user.partner_id
		if responsible_id:
			model_id = self.env.ref('purchase.model_purchase_order').id
			if approval_type:
				approval_user_name = _('<a href="#" data-oe-id="%s" data-oe-model="res.partner">%s</a>') % (
				approval_name.id, approval_name.name)
				message = _('Purchase Order "%s" is waiting for %s approval from %s .') % (
				self.name, approval_type, approval_user_name)
				self.message_post(
					body=message,
					subtype='mail.mt_comment',
					message_type="notification"
				)
				try:
					activity_type_id = self.env.ref('mail.mail_activity_data_todo').id
				except ValueError:
					activity_type_id = False
				activity = self.env['mail.activity'].create({
					'activity_type_id': activity_type_id,
					'user_id': responsible_id.id,
					'res_id': self.id,
					'res_model_id': model_id,
					'date_deadline': datetime.now().date(),
					'purchase_approval': approval_type
				})
		return True

	def remove_activity_log(self):
		for rec in self:
			approval_type = False
			if rec.state == 'approval_1':
				approval_type = 'Approval_1'
			elif rec.state == 'approval_2':
				approval_type = 'Approval_2'
			model_id = self.env.ref('purchase.model_purchase_order').id
			try:
				activity_type_id = self.env.ref('mail.mail_activity_data_todo').id
			except ValueError:
				activity_type_id = False
			if approval_type:
				activity_ids = self.env['mail.activity'].search([
					('purchase_approval', '=', approval_type),
					('res_id', '=', rec.id),
					('res_model_id', '=', model_id),
					('activity_type_id', '=', activity_type_id)
				])
				for activity_id in activity_ids:
					activity_id.action_feedback()
		return True

	def set_state_approved(self):
		approval_type = None
		state_type = 'Approved'
		if self:
			self.remove_activity_log()
			if self.state == 'approval_1':
				approval_type = 'Approval_1'
				self.write({
					'state': 'approval_2',
					'approver_1_state': 'done',
					'approver_1_approved_date': datetime.now()
				})
			elif self.state == 'approval_2':
				approval_type = 'Approval_2'
				self.button_approve()
				self.write({
					'approver_2_state': 'done',
					'approver_2_approved_date': datetime.now()
				})
				self.send_approved_purchase_order()
			message = '%s "%s" is updated for %s approval with %s state ' % ("Purchase Order",
																			 self.name,
																			 approval_type,
																			 state_type
																			 )
			if self.comments:
				name = self.comments and self.comments.strip()
				message += "with bellow comments<br/>%s " % (name)
			self.message_post(
				body=message,
				subtype='mail.mt_comment',
				message_type="notification"
			)
			self.comments = ''
			self.activity_log()

	def set_state_hold(self):
		approval_type = None
		state_type = 'On Hold'
		if self:
			self.remove_activity_log()
			if self.state == 'approval_1':
				approval_type = 'Approval_1'
				self.write({
					'state': 'draft',
					'approver_1_state': 'hold',
					'approver_1_approved_date': datetime.now()
				})
			elif self.state == 'approval_2':
				approval_type = 'Approval_2'
				self.write({
					'state': 'draft',
					'approver_1_state': 'pending',
					'approver_2_state': 'hold',
					'approver_2_approved_date': datetime.now()
				})
			message = '%s "%s" is updated for %s approval with %s state ' % ("Purchase Order",
																			 self.name,
																			 approval_type,
																			 state_type
																			 )
			if self.comments:
				name = self.comments and self.comments.strip()
				message += "with bellow comments<br/>%s " % (name)
			self.message_post(
				body=message,
				subtype='mail.mt_comment',
				message_type="notification"
			)
			self.comments = ''
			self.activity_log()

	def set_state_cancel(self):
		approval_type = None
		state_type = 'Rejected'
		if self:
			self.remove_activity_log()
			if self.state == 'approval_1':
				approval_type = 'Approval_1'
				self.write({
					'state': 'cancel',
					'approver_1_state': 'cancelled',
					'approver_1_approved_date': datetime.now()
				})
			elif self.state == 'approval_2':
				approval_type = 'Approval_2'
				self.write({
					'state': 'cancel',
					'approver_2_state': 'cancelled',
					'approver_2_approved_date': datetime.now()
				})
			message = '%s "%s" is updated for %s approval with %s state ' % (
				"Purchase Order",
				self.name,
				approval_type,
				state_type
			)
			if self.comments:
				name = self.comments and self.comments.strip()
				message += "with bellow comments<br/>%s " % name
			self.message_post(
				body=message,
				subtype='mail.mt_comment',
				message_type="notification"
			)
			self.comments = ''

	def button_draft(self):
		res = super(PurchaseOrderNew, self).button_draft()
		for rec in self:
			rec.is_app_manager = False
			rec.approver_1_approved_date = False
			rec.approver_2_approved_date = False
			rec.approver_1_state = 'pending'
			rec.approver_2_state = 'pending'
		return res

	def button_sent_to_approve(self):
		for rec in self:
			rec.write({
				'state': 'approval_1',
				'approver_1_state': 'pending',
				'approver_1_date': False,
				'approver_2_state': 'pending',
				'approver_2_date': False,
				'submission_date': datetime.now(),
			})
			rec.activity_log()
		return True

	def send_approved_purchase_order(self):
		user = self.create_uid
		report_id = 'purchase.action_report_purchase_order'
		pdf = self.env.ref(report_id).render_qweb_pdf(self.ids)
		b64_pdf = base64.b64encode(pdf[0])
		pdf_name = self.name
		attachment = self.env['ir.attachment'].create({
			'name': pdf_name,
			'type': 'binary',
			'datas': b64_pdf,
			'datas_fname': pdf_name + '.pdf',
			'store_fname': pdf_name,
			'res_model': self._name,
			'res_id': self.id,
			'mimetype': 'application/pdf'
		})
		subject = "Purchase {0}".format(self.name)
		name = user.name
		body_html = """Dear <strong>{0}</strong> <br/><br/>
			Here is in attachment a purchase order <strong>{1}</strong> amounting in {2} {3} from {4}.<br/><br/>
			Thank you.<br/>
		""".format(name, self.name, self.amount_total, self.currency_id.symbol, self.company_id.name)
		email_to = user.partner_id.email
		mail_values = {
			'email_from': self.env.user.login,
			'email_to': email_to,
			'subject': subject,
			'body_html': body_html,
			'state': 'outgoing',
			'auto_delete': True,
		}
		mail_id = self.env['mail.mail'].create(mail_values)
		mail_id.attachment_ids = [(4, attachment.id)]
		self.create_note_for_invoice(mail_values, attachment)
		mail_id.send()

	def create_note_for_invoice(self, vals, attachment):
		new_vals = {
			'email_from': vals.get('email_from', False),
			'subject': vals.get('subject', False),
			'message_type': 'comment',
			'model': 'purchase.order',
			'parent_id': self.id,
			'record_name': self.name,
			'body': vals.get('body_html'),
			'res_id': self.id,
			'subtype_id': self.env.ref('mail.mt_note').id,
		}
		self.env['mail.message'].create(new_vals)


class MailActivity(models.Model):
	_inherit = 'mail.activity'

	purchase_approval = fields.Char(string="Purchase Approval")


class IrAttachment(models.Model):
	_inherit = 'ir.attachment'

	purchase_id = fields.Many2one('purchase.order', string='Purchase Order')
