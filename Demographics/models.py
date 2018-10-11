from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Scott Claessens'

doc = """
Demographics
"""


class Constants(BaseConstants):
    name_in_url = 'Demographics'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


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
