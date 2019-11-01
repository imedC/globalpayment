# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from werkzeug import urls
from odoo.addons.e3k_payment_globalpay.controllers.main import GlobalPaymentController
from globalpayments.api import ServicesConfig, ServicesContainer
import time
import hashlib


class AcquirerGlobal(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('globalpayment', 'Global Payment')])
    gp_id_account = fields.Char('Account ID', required_if_provider='globalpayment', groups='base.group_user')
    gp_seller_account = fields.Char(
        'Merchant ID', groups='base.group_user',
        help='The Merchant ID is used to ensure communications coming from Global Payment are valid and secured.')
    gp_shared_secret_account = fields.Char('Shared Secret')

    def _get_globalpayment_urls(self, environment):

        return {
            'global_form_url': 'https://pay.sandbox.realexpayments.com/pay',
        }

    # @api.multi
    # def globalpayment_form_generate_values(self, values):
    #
    #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     globalpayment_tx_values = dict(values)
    #     order = self.env['sale.order'].search([], limit=1)
    #     reference = ''
    #     if self.env['payment.transaction'].search(
    #             [('acquirer_id', '=', self.env.ref('payment.payment_acquirer_global').id),
    #              ('sale_order_id', '=', order.id)], limit=1):
    #         reference += self.env['payment.transaction'].search(
    #             [('acquirer_id', '=', self.env.ref('payment.payment_acquirer_global').id),
    #              ('sale_order_id', '=', order.id)], limit=1).sale_order_id.name
    #     else:
    #         self.env['payment.transaction'].create({'sale_order_id': order.id, 'reference': order.name,
    #                                                 'acquirer_id': self.env.ref('payment.payment_acquirer_global').id,
    #                                                 'amount':values['amount'],'currency_id':values['currency_id'],'partner_country_id':values['partner_country_id']})
    #         reference+=order.name
    #     timestamp = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    #     add_second = time.strftime("%S", time.gmtime())
    #     order_id = reference + add_second
    #     str_to_hash = timestamp + '.lkvape.' + order_id + '.' + str(values['amount']).replace('.', '') + '.' + values[
    #         'currency'].name
    #     str_hashed = hashlib.sha1((str_to_hash).encode('utf8'))
    #     str_other_to_hash = hashlib.sha1((str_hashed.hexdigest() + '.secret').encode('utf8'))
    #     hash = str_other_to_hash.hexdigest()
    #     globalpayment_tx_values.update({
    #         'merchant_id': self.gp_seller_account,
    #         'account_id': self.gp_id_account,
    #         'shared_secret': self.gp_shared_secret_account,
    #         'global_amount': str(values['amount']).replace('.', ''),
    #         'global_currency': values['currency'] and values['currency'].name or '',
    #         'order_id': order_id,
    #         'invoice_number': values['reference'],
    #         'success_url': urls.url_join(base_url, GlobalPaymentController._success_url),
    #         'timestamp': timestamp,
    #         'SHA1HASH': hash
    #
    #     })
    #     print('****global****', globalpayment_tx_values)
    #
    #     return globalpayment_tx_values


    def configure_client(self):
        config = ServicesConfig()
        global_payment = self.env['payment.acquirer'].search(
            [('id', '=', self.env.ref('payment.payment_acquirer_global').id)])
        config.merchant_id = global_payment.gp_seller_account
        config.account_id = global_payment.gp_id_account
        config.shared_secret = global_payment.gp_shared_secret_account
        config.service_url = 'https://api.sandbox.realexpayments.com/epage-remote.cgi'
        ServicesContainer.configure(config)
        print(global_payment.gp_seller_account)
        print(config.shared_secret)
