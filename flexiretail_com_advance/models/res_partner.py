# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_remain_credit_limit(self):
        for partner in self:
            total_credited = 0
            orders = self.env['pos.order'].search([('partner_id', '=', partner.id),
                                                   ('state', '=', 'draft')])
            for order in orders:
                total_credited += order.amount_due
            partner.remaining_credit_limit = partner.credit_limit - total_credited

    @api.multi
    @api.depends('used_ids', 'recharged_ids')
    def compute_amount(self):
        total_amount = 0
        for ids in self:
            for card_id in ids.card_ids:
                total_amount += card_id.card_value
            ids.remaining_amount =  total_amount

    @api.one
    @api.depends('wallet_lines')
    def _calc_remaining(self):
        total = 0.00
        for s in self:
            for line in s.wallet_lines:
                total += line.credit - line.debit
        self.remaining_wallet_amount = total;

    card_ids = fields.One2many('aspl.gift.card', 'customer_id', string="List of card")
    used_ids = fields.One2many('aspl.gift.card.use', 'customer_id', string="List of used card")
    recharged_ids = fields.One2many('aspl.gift.card.recharge', 'customer_id', string="List of recharged card")
    remaining_amount = fields.Char(compute=compute_amount , string="Remaining Amount", readonly=True)

    wallet_lines = fields.One2many('wallet.management', 'customer_id', string="Wallet", readonly=True)
    remaining_wallet_amount = fields.Float(compute="_calc_remaining",string="Remaining Amount", readonly=True, store=True)
    prefer_ereceipt = fields.Boolean('Prefer E-Receipt')
    remaining_credit_limit = fields.Float("Remaining Credit Limit", compute="_compute_remain_credit_limit")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: