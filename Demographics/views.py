from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


def vars_for_all_templates(self):
    return {'treatment': self.player.treatment}


class Prolific(Page):
    form_model = models.Player
    form_fields = ['prolificID']


class Demographics(Page):
    form_model = models.Player
    form_fields = ['age', 'sex', 'language']


page_sequence = [
    Prolific,
    Demographics
]
