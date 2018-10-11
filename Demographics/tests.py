from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (views.Prolific, {'prolificID': "AAA11"})
        yield (views.Demographics, {'age': 25, 'sex': 1, 'language': 1})
