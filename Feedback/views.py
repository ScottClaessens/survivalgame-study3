from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class AttentionCheck(Page):
    form_model = models.Player
    form_fields = ['attention']


class ExitSurvey(Page):
    form_model = models.Player
    form_fields = [
                   #  'feel_bad_need',
                   'feel_bad_ask',
                   'fairness',
                   'risk_pooling_true',
                   'risk_pooling_false',
                   'why_give']

    def before_next_page(self):
        #  if self.player.feel_bad_need is not None:
        #      self.participant.payoff += c(1)
        if self.player.feel_bad_ask is not None:
            self.participant.payoff += c(1)
        if self.player.fairness is not None:
            self.participant.payoff += c(1)
        if self.player.risk_pooling_true is not None:
            self.participant.payoff += c(1)
        if self.player.risk_pooling_false is not None:
            self.participant.payoff += c(1)
        if self.player.why_give is not "":
            self.participant.payoff += c(1)


class Feedback(Page):
    form_model = models.Player
    form_fields = ['rushed',
                   'waiting',
                   'instructions',
                   'feedback']

    def before_next_page(self):
        if self.player.rushed is not None:
            self.participant.payoff += c(1)
        if self.player.waiting is not None:
            self.participant.payoff += c(1)
        if self.player.instructions is not None:
            self.participant.payoff += c(1)
        if self.player.feedback is not "":
            self.participant.payoff += c(1)


class ProlificFinal(Page):
    pass


page_sequence = [
    AttentionCheck,
    ExitSurvey,
    Feedback,
    ProlificFinal
]
