from odoo import models, fields, api
import logging
import secrets

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = 'hr.employee'

    invite_token = fields.Char('Invite Token')
    portal_uid = fields.Char('Portal UID')
    invite_url = fields.Char(compute='get_invite_url')

    def generate_invite_token(self):
        if self.portal_uid == False and self.invite_token == False:
            self.invite_token = secrets.token_urlsafe(32)
            # sending email with template
            # fetch the template id for sending the mail
            template_id = self.env.ref('edari_timesheet.edari_portal_invite_email_template').id
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(self.id, force_send=True)
            # Sending email without a template
            # subject = "Edari Portal Invitation URL "
            # # name = self.name
            # body_html = """Dear Thank you.<br/>"""
            # # email_to = self.work_email
            # email_to = "irshadcom.26@gmail.com"
            # vals = {
            #     'email_from': email_to,
            #     'email_to': email_to,
            #     'subject': subject,
            #     'body_html': body_html,
            #     'state': 'outgoing',
            #     'auto_delete': False,
            # }
            # mail_id = self.env['mail.mail'].create(vals)
            # new_vals = {
            #     'email_from': vals.get('email_from', False),
            #     'subject': vals.get('subject', False),
            #     'message_type': 'comment',
            #     'model': 'hr.employee',
            #     'parent_id': self.id,
            #     'record_name': self.name,
            #     'body': vals.get('body_html'),
            #     'res_id': self.id,
            #     'subtype_id': self.env.ref('mail.mt_note').id,
            # }
            # self.env['mail.message'].create(new_vals)
            # mail_id.send()

    @api.depends('invite_token')
    def get_invite_url(self):
        for record in self:
            record.invite_url = False
            if record.invite_token:
                db_name = self._cr.dbname
                if "staging" in db_name:
                    record.invite_url = "https://portal-staging.edarihub.com?type=employee&invite_token={}".format(
                        self.invite_token)
                else:
                    record.invite_url = "https://portal.edarihub.com?type=employee&invite_token={}".format(
                        self.invite_token)

