from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Earnings(Page):
    def vars_for_template(self):
        return {'final_payment': self.participant.payoff_plus_participation_fee,
                'participation_fee': self.session.config['participation_fee'],
                'payment_for_wait': c(self.participant.vars['payment_for_wait']).to_real_world_currency(self.session),
                'payment_from_game': c(self.participant.vars['payment_from_game']).to_real_world_currency(self.session)}


page_sequence = [
    Earnings,
]
