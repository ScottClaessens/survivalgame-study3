from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class PlayingTheGame1(Page):
    def vars_for_template(self):
        return {'initial': self.session.config['initialherd'],
                'minherd': self.session.config['minherd']}


class PlayingTheGame2(Page):
    def vars_for_template(self):
        return {'years': self.session.config['years_before_death'],
                'minherd': self.session.config['minherd']}


class Manipulation(Page):
    def vars_for_template(self):
        return {'visible_give': self.session.config['visible_give'],
                'visible_ask': self.session.config['visible_ask']}


class Earnings(Page):
    def vars_for_template(self):
        return {'base_pay': self.session.config['participation_fee']}


class BeginExample(Page):
    pass


page_sequence = [
    Introduction,
    PlayingTheGame1,
    PlayingTheGame2,
    Manipulation,
    Earnings,
    BeginExample,
]
