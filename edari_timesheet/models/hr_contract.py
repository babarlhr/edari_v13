from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Contract(models.Model):
    _inherit = 'hr.contract'

    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", copy=False, ondelete='set null',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", check_company=True,
        help="Analytic account to which this project is linked for financial management. "
             "Use an analytic account to record cost and revenue on your project.")
    
    timesheet_cycle = fields.Selection([
        ('monthly','Monthly'),
        ('weekly','Weekly'),
        ], string='Timesheet Cycle', default='monthly')
    
    timesheet_mode = fields.Selection([
        ('daily','Daily'),
        ('hourly','Hourly'),
        ], string='Timesheet Mode', default='daily')

    customer = fields.Many2one(related="cost_card.job_pos.customer")
    timesheet_approver_1 = fields.Many2one('res.partner', string='Timesheet Approver 1', tracking=True, domain="['&', '|', ('company_id', '=', False), ('company_id', '=', company_id), ('type', '=', 'contact'), ('parent_id', '=', customer)]")
    timesheet_approver_2 = fields.Many2one('res.partner', string='Timesheet Approver 2', tracking=True, domain="['&', '|', ('company_id', '=', False), ('company_id', '=', company_id), ('type', '=', 'contact'), ('parent_id', '=', customer)]")
    
    @api.model
    def create(self, values):
        """ Create an analytic account for contract
            Note: create it before calling super() to avoid raising the ValidationError from _check_allow_timesheet
        """
        if not values.get('analytic_account_id'):
            analytic_account = self._create_analytic_account_from_values(values)
            values['analytic_account_id'] = analytic_account.id
        response = super(Contract, self).create(values)
        return response

    def write(self, values):
        """ Create an analytic account for contract
            Note: create it before calling super() to avoid raising the ValidationError from _check_allow_timesheet
        """
        response = super(Contract, self).write(values)
        if not self.analytic_account_id and not values.get('analytic_account_id'):
            self._create_analytic_account()
        return response

    def _create_analytic_account_from_values(self, values):
        analytic_account = self.env['account.analytic.account'].create({
            'name': values.get('name', 'Unknown Analytic Account'),
            'company_id': values.get('company_id') or self.env.company.id,
            'partner_id': values.get('partner_id'),
            'active': True,
        })
        return analytic_account

    def _create_analytic_account(self):
        for contract in self:
            analytic_account = self.env['account.analytic.account'].create({
                'name': contract.name,
                'company_id': contract.company_id.id,
                'partner_id': contract.customer.id,
                'active': True,
            })
            contract.write({'analytic_account_id': analytic_account.id})