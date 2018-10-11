from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.session.config['visible_ask']:
            if self.session.config['visible_give']:
                x = 1
            else:
                x = 2
        else:
            if self.session.config['visible_give']:
                x = 3
            else:
                x = 4
        yield (views.Comprehension,
               {'q1': self.session.config['minherd'],
                'q2': self.session.config['years_before_death'],
                'q3': 1,
                'q4': 2,
                'q5': 3,
                'q6': 5,
                'q7': x})
        yield (views.BeginStudy)
