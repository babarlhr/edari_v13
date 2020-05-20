from odoo import models, fields, api
import logging, secrets

_logger = logging.getLogger(__name__)

class Applicant(models.Model):
    _inherit = 'hr.applicant'

    invite_token = fields.Char('Invite Token')
    portal_uid = fields.Char('Portal UID')
    invite_url = fields.Char(compute='get_invite_url')

    def generate_invite_token(self):
        if self.portal_uid == False and self.invite_token == False:
            self.invite_token = secrets.token_urlsafe(32)

    @api.depends('invite_token')
    def get_invite_url(self):
        for record in self:
            record.invite_url = False
            if record.invite_token:
                record.invite_url = "https://portal.edarihub.com?type=applicant&invite_token={}".format(
                    self.invite_token)