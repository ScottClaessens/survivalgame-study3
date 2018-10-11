from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Comprehension(Page):
    form_model = models.Player
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7']

    #
    # The "correct" answers to comprehension questions, and error text
    #
    def q1_error_message(self, value):
        if not value == self.session.config['minherd']:
            return 'This is incorrect. The minimum threshold is 64 cattle.'

    def q2_error_message(self, value):
        if not value == self.session.config['years_before_death']:
            return 'This is incorrect. If you are under the threshold for 3 years, you die and are ' \
                   'removed from the game.'

    def q3_error_message(self, value):
        if not value == 1:
            return 'This is incorrect. Each year proceeds as follows: 1) herd births and deaths, ' \
                   '2) ask for cattle, and 3) the year ends.'

    def q4_error_message(self, value):
        if not value == 2:
            return 'This is incorrect. After herd births and deaths, players can ask for cattle, ' \
                   'and respond to requests from others.'

    def q5_error_message(self, value):
        if not value == 3:
            return 'This is incorrect. Your payment from the game depends on BOTH the amount of cattle ' \
                   'you have at the end of each year, AND the number of years you survive for.'

    def q6_error_message(self, value):
        if not value == 5:
            return 'This is incorrect. Your overall payment from the experiment comes from ALL OF THE ABOVE.'

    def q7_error_message(self, value):
        if self.session.config['visible_ask']:
            if self.session.config['visible_give']:
                if not value == 1:
                    return 'This is incorrect. The other player can see how many cattle you currently have both ' \
                           'when they ask you for cattle AND when they decide whether to give you cattle.'
            else:
                if not value == 2:
                    return 'This is incorrect. The other player can see how many cattle you currently have only ' \
                           'when they ask you for cattle.'
        else:
            if self.session.config['visible_give']:
                if not value == 3:
                    return 'This is incorrect. The other player can see how many cattle you currently have only ' \
                           'when they decide whether to give you cattle.'
            else:
                if not value == 4:
                    return 'This is incorrect. The other player can NEVER see how many cattle you currently have.'

    def before_next_page(self):
        self.participant.payoff += c(14)


class BeginStudy(Page):
    pass


page_sequence = [
    Comprehension,
    BeginStudy
]
