from otree.api import Currency as c, currency_range
from otree.api import Submission
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (views.AttentionCheck, {'attention': 6})
        yield (views.ExitSurvey)
        yield (views.Feedback)
        yield Submission(views.ProlificFinal, check_html=False)

