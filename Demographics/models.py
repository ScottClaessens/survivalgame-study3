from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import shuffle


author = 'Scott Claessens'

doc = """
Demographics
"""


class Constants(BaseConstants):
    name_in_url = 'Demographics'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def before_session_starts(self):
        # randomisation
        treatments = [1, 2, 3, 4]
        shuffle(treatments)
        treatments = treatments * int((len(self.get_players())/4))
        i = 0
        for p in self.get_players():
            if treatments[i] == 1:
                p.treatment = 1
                p.participant.vars['treatment'] = 1
                p.participant.vars['visible_ask'] = True
                p.participant.vars['visible_give'] = True
            elif treatments[i] == 2:
                p.treatment = 2
                p.participant.vars['treatment'] = 2
                p.participant.vars['visible_ask'] = True
                p.participant.vars['visible_give'] = False
            elif treatments[i] == 3:
                p.treatment = 3
                p.participant.vars['treatment'] = 3
                p.participant.vars['visible_ask'] = False
                p.participant.vars['visible_give'] = True
            elif treatments[i] == 4:
                p.treatment = 4
                p.participant.vars['treatment'] = 4
                p.participant.vars['visible_ask'] = False
                p.participant.vars['visible_give'] = False
            i += 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #
    # Prolific ID
    #
    prolificID = models.StringField()
    #
    # Demographic questions = age, sex and primary language
    #
    age = models.PositiveIntegerField(
        min=18,max=100)

    sex = models.IntegerField(
        choices=[
            [1, "Male"],
            [2, "Female"],
            [3, "Other"],
        ],
        widget=widgets.RadioSelect,
    )

    language = models.IntegerField(
        choices=[
            [1, "English"],
            [2, "Other"],
        ],
        widget=widgets.RadioSelect,
    )

    treatment = models.IntegerField()
