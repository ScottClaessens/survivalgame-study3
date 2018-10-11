from otree.api import Currency as c, currency_range, Submission
from . import views
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (views.NewYear)
        yield (views.GrowthAndShock)
        yield (views.Request, {'request': random.choice([True, False])})
        if self.player.request:
            yield (views.RequestAmount, {'request_amount': c(10)})
            yield (views.AllTransfers)
        else:
            yield (views.NoTransfers)
        yield (views.EndYear)
