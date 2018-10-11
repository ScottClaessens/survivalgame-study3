from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from django.db import models as djmodels
from django.db.models import Q, Sum

author = 'Scott Claessens'

doc = """Example Year"""


class Constants(BaseConstants):
    name_in_url = 'ExampleYear'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.participant.vars['example_year_herd_size'] = self.session.config['initialherd']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def set_growth(self):
        # herd size always grows by 4 cattle in the example year
        self.participant.vars['example_year_herd_size'] = self.participant.vars['example_year_herd_size'] + c(4)

    def set_transfer(self):
        # if player requests cattle, other player always gives 10 cattle
        # in the example year (regardless of how much asked for)
        self.participant.vars['example_year_herd_size'] = self.participant.vars['example_year_herd_size'] + c(10)

    request = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No'],
                 ],
        widget=widgets.RadioSelect(),
        verbose_name="Would you like to ask for cattle from the other player?"
    )

    request_amount = models.CurrencyField(
        min=c(1),
        verbose_name="How many cattle would you like to ask this player for?"
    )
