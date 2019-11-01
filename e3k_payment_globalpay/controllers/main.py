# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from werkzeug import urls
from globalpayments.api.payment_methods import CreditCardData
from globalpayments.api.entities import Transaction
import werkzeug
import logging
import pprint
_logger = logging.getLogger(__name__)
from globalpayments.api.entities.exceptions import GatewayException

class GlobalPaymentController(http.Controller):

    @http.route('/payment/global', type='http',csrf=False, auth='public', website=True)
    def global_create_json(self, **kwargs):
        _logger.info('Beginning global payment form_feedback with post data %s', pprint.pformat(kwargs))
        cr, uid, context = request.cr, request.uid, request.context
        transaction_obj = request.env['payment.transaction']
        order = request.website.sale_get_order()
        tx = request.website.sale_get_transaction()
        print(order,tx)
        request.env['payment.acquirer'].configure_client()
        card = CreditCardData()
        card.number = kwargs['card-number']
        card.exp_month = kwargs['expiry-date-mm']
        card.exp_year = kwargs['expiry-date-yy']
        card.cvn = kwargs['cvn']
        card.card_holder_name = kwargs['cardholder-name']
        try:
            check_verification = card.verify() \
                .with_currency(tx.currency_id.name) \
                .execute()
            response = check_verification.response_code
            print('****', response)
            card.charge(tx.amount) \
                .with_currency(tx.currency_id.name) \
                .execute()
            if tx:
                          # button cliked but no more info -> rewrite on tx or create a new one ?
                tx.write({
                        'acquirer_id': request.env.ref('payment.payment_acquirer_global').id,
                        'amount': order.amount_total,
                        'state':'pending'
                    })
            else:
                tx_id = transaction_obj.sudo().create({
                    'acquirer_id': kwargs['acquirer_id'],
                    'type': 'form',
                    'amount': order.amount_total,
                    'currency_id': order.pricelist_id.currency_id.id,
                    'partner_id': order.partner_id.id,
                    'partner_country_id': order.partner_id.country_id.id,
                    'reference': order.name,
                    'sale_order_id': order.id,
                    'state':'done'
                }, context=context)
                request.session['sale_transaction_id'] = tx_id

                # update quotation
            order.sudo().action_confirm()
            return request.render('e3k_payment_globalpay.confirm_g_payment',
                                  {'data': kwargs, 'order': tx.sale_order_id})
        except GatewayException as e:
            if int(e.response_code) == 506:
                _logger.info('Bad Geteway****506****')

