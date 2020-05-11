from odoo import models, fields, api
import logging, secrets

_logger = logging.getLogger(__name__)

class Contact(models.Model):
    _inherit = 'res.partner'

    # invite_token = fields.Char('Invite Token')
    #
    # def generate_invite_token(self):
    #     self.invite_token = secrets.token_urlsafe(32)