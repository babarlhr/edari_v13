from odoo import models, fields, api
import logging, secrets

_logger = logging.getLogger(__name__)

class ContactExtension(models.Model):
    _inherit = 'res.partner'

    invite_token = fields.Char('Invite Token')
    portal_uid = fields.Char('Portal UID')
    invite_url = fields.Char(compute='get_invite_url')

    # def generate_invite_token(self):
    #     if self.portal_uid == False and self.invite_token == False:
    #         self.invite_token = secrets.token_urlsafe(32)

    def generate_invite_token(self):
        if self.portal_uid == False and self.invite_token == False:
            self.invite_token = secrets.token_urlsafe(32)
            # sending email with template
            # fetch the template id for sending the mail
            template_id = self.env.ref('edari_timesheet.edari_portal_invite_email_template_client').id
            template = self.env['mail.template'].browse(template_id)
            template.send_mail(self.id, force_send=True)

    @api.depends('invite_token')
    def get_invite_url(self):
        for record in self:
            record.invite_url = False
            if record.invite_token:
                db_name = self._cr.dbname
                if "staging" in db_name:
                    record.invite_url = "https://clients-staging.edarihub.com?type=customer&invite_token={}".format(
                        self.invite_token)
                else:
                    record.invite_url = "https://clients.edarihub.com?type=customer&invite_token={}".format(
                        self.invite_token)