from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Scott Claessens'

doc = """
Comprehension Questions
"""


class Constants(BaseConstants):
    name_in_url = 'Comprehension'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #
    # The comprehension questions, with options
    #
    q1 = models.PositiveIntegerField(
        verbose_name="What is the minimum herd size survival threshold?"
    )

    q2 = models.PositiveIntegerField(
        verbose_name="A player dies if they remain under the threshold for how many years?"
    )

    q3 = models.PositiveIntegerField(
        verbose_name="Each year proceeds in which of the following orders?",
        choices=[
            [1, "Herd births and deaths -> Ask for cattle -> End of year"],
            [2, "Ask for cattle -> Herd births and deaths -> End of year"],
            [3, "Herd births and deaths -> End of year -> Ask for cattle"],
            [4, "Ask for cattle -> End of year -> Herd births and deaths"],
        ],
        widget=widgets.RadioSelect
    )

    q4 = models.PositiveIntegerField(
        verbose_name="After herd births and deaths...",
        choices=[
            [1, "The year ends"],
            [2, "Players can ask for cattle, and respond to requests from others"],
            [3, "Another disaster strikes"],
        ],
        widget=widgets.RadioSelect
    )

    q5 = models.PositiveIntegerField(
        verbose_name="Your payment for how you play the game depends on...",
        choices=[
            [1, "The amount of cattle you begin each year with"],
            [2, "The number of years you survive"],
            [3, "BOTH the amount of cattle you begin each year with AND the number of years you survive"],
        ],
        widget=widgets.RadioSelect
    )

    q6 = models.PositiveIntegerField(
        verbose_name="Overall payment from this experiment comes from...",
        choices=[
            [1, "The initial participation fee"],
            [2, "Completing the comprehension questions"],
            [3, "Time spent waiting to be paired with another player"],
            [4, "Performance in the game"],
            [5, "All of the above"],
        ],
        widget=widgets.RadioSelect
    )

    q7 = models.PositiveIntegerField(
        verbose_name="The other player in the game can see how many cattle I have...",
        choices=[
            [1, "Both when they ask me for cattle AND when they decide whether to give me cattle"],
            [2, "ONLY when they ask me for cattle"],
            [3, "ONLY when they decide whether to give me cattle"],
            [4, "The other player can NEVER see how many cattle I have"]
        ],
        widget=widgets.RadioSelect
    )
