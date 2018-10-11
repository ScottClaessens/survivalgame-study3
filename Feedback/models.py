from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Scott Claessens'

doc = """
Feedback
"""


class Constants(BaseConstants):
    name_in_url = 'Feedback'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #
    # Attention check, to ensure that participants are paying attention
    #
    attention = models.PositiveIntegerField(
        verbose_name="What was this study about?",
        choices=[
            [1, "Managing resources"],
            [2, "Managing money"],
            [3, "Managing cattle"],
            [4, "Issues of religion"],
            [5, "Issues of society"],
            [6, "Issues of geography"],
        ],
        widget=widgets.RadioSelect
    )

    #
    # Empathy questions
    #
    #

    # obligation = models.PositiveIntegerField(
    #    verbose_name="I felt obligated to give to when my partner asked for cattle.",
    #    choices=[
    #        [1, "Strongly agree"],
    #        [2, "Agree"],
    #        [3, "Neither agree nor disagree"],
    #        [4, "Disagree"],
    #        [5, "Strongly disagree"]
    #    ],
    #    widget=widgets.RadioSelect,
    #    blank=True
    # )

    #feel_bad_need = models.PositiveIntegerField(
    #    verbose_name="I felt bad for my partner when they were below the survival threshold.",
    #    choices=[
    #        [5, "Strongly agree"],
    #        [4, "Agree"],
    #        [3, "Neither agree nor disagree"],
    #        [2, "Disagree"],
    #        [1, "Strongly disagree"]
    #    ],
    #    widget=widgets.RadioSelect,
    #    blank=True
    #)

    feel_bad_ask = models.PositiveIntegerField(
        verbose_name="I felt bad for my partner when they asked me for cattle.",
        choices=[
            [5, "Strongly agree"],
            [4, "Agree"],
            [3, "Neither agree nor disagree"],
            [2, "Disagree"],
            [1, "Strongly disagree"]
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    fairness = models.PositiveIntegerField(
        verbose_name="I felt that it was fair to give cattle to my partner when asked me for cattle.",
        choices=[
            [5, "Strongly agree"],
            [4, "Agree"],
            [3, "Neither agree nor disagree"],
            [2, "Disagree"],
            [1, "Strongly disagree"]
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    risk_pooling_true = models.PositiveIntegerField(
        verbose_name="One way to survive for more years was to give "
                     "cattle to my partner when they asked.",
        choices=[
            [5, "Strongly agree"],
            [4, "Agree"],
            [3, "Neither agree nor disagree"],
            [2, "Disagree"],
            [1, "Strongly disagree"]
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    risk_pooling_false = models.PositiveIntegerField(
        verbose_name="One way to survive for more years was to keep "
                     "all the cattle to myself.",
        choices=[
            [5, "Strongly agree"],
            [4, "Agree"],
            [3, "Neither agree nor disagree"],
            [2, "Disagree"],
            [1, "Strongly disagree"]
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    why_give = models.TextField(
        blank=True
    )

    #
    # Feedback questions (blank=True means participants do not have to answer)
    #
    rushed = models.PositiveIntegerField(
        verbose_name="I felt under time pressure to make decisions during the game.",
        choices=[
            [5, "Strongly agree"],
            [4, "Agree"],
            [3, "Neither agree nor disagree"],
            [2, "Disagree"],
            [1, "Strongly disagree"]
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    waiting = models.PositiveIntegerField(
        verbose_name="I felt that I was waiting a long time for the other player.",
        choices=[
            [5, "Strongly agree"],
            [4, "Agree"],
            [3, "Neither agree nor disagree"],
            [2, "Disagree"],
            [1, "Strongly disagree"]
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    instructions = models.PositiveIntegerField(
        verbose_name="The instructions for the game were easy to understand.",
        choices=[
            [5, "Strongly agree"],
            [4, "Agree"],
            [3, "Neither agree nor disagree"],
            [2, "Disagree"],
            [1, "Strongly disagree"]
        ],
        widget=widgets.RadioSelect,
        blank=True
    )

    feedback = models.TextField(
        blank=True
    )



