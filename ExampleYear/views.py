from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player
import django
from django.db.models import Q


def vars_for_all_templates(self):
    return {'herd_size_for_chart': int(self.player.participant.vars['example_year_herd_size']),
            'visible_ask': self.session.config['visible_ask'],
            'visible_give': self.session.config['visible_give'],
            'minherd': self.session.config['minherd'],
            'charts': self.session.config['charts'],
            'summary_box': self.session.config['summary_box'],
            }


class NewYear(Page):
    def before_next_page(self):
        # herd grows before the next page
        self.player.set_growth()


class GrowthAndShock(Page):
    def vars_for_template(self):
        return {'herd_size_initial': self.session.config['initialherd'],
                'herd_size_after_growth': self.participant.vars['example_year_herd_size'],
                'herd_size_after_shock': self.participant.vars['example_year_herd_size'],
                }


class Request(Page):
    form_model = models.Player
    form_fields = ['request']

    def vars_for_template(self):
        return {'herd_size_after_shock': self.participant.vars['example_year_herd_size']}


class RequestAmount(Page):
    form_model = models.Player
    form_fields = ['request_amount']

    def is_displayed(self):
        # page only displayed if player wanted to request cattle
        return self.player.request

    def vars_for_template(self):
        return {'herd_size_after_shock': self.participant.vars['example_year_herd_size'],
                'request': self.player.request}

    def before_next_page(self):
        # transfers are done before the next page
        self.player.set_transfer()


class NoTransfers(Page):
    def is_displayed(self):
        # page only displayed if player did not request
        return self.player.request is False

    def vars_for_template(self):
        return {'herd_size_after_shock': self.participant.vars['example_year_herd_size']}


class AllTransfers(Page):
    def vars_for_template(self):
        return {'herd_size_after_transfers': self.participant.vars['example_year_herd_size'],
                'request': self.player.request,
                'request_amount': self.player.request_amount
                }

    def is_displayed(self):
        # page only displayed if player wanted to request cattle
        return self.player.request


class EndYear(Page):
    def vars_for_template(self):
        # calculating the other player's herd size, based on whether cattle were sent or not
        if self.player.request:
            P2_herdsize = self.participant.vars['example_year_herd_size'] - c(20)
        else:
            P2_herdsize = self.participant.vars['example_year_herd_size']
        return {'herd_size_after_transfers': self.participant.vars['example_year_herd_size'],
                'P2_herd_size_after_transfers': P2_herdsize,
                'request': self.player.request,
                'request_amount': self.player.request_amount}


page_sequence = [
    NewYear,
    GrowthAndShock,
    Request,
    RequestAmount,
    NoTransfers,
    AllTransfers,
    EndYear,
]
