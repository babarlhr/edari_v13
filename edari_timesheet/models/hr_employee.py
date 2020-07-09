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
            # fetch the template id for sending the mail
            template_id = self.env.ref('edari_timesheet.portal_invite_email_template').id
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(self.id, force_send=True)

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

