from otree.api import Currency as c, currency_range, Submission
from . import views
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.player.round_number == 1:
            yield (views.Initial)
        if self.player.is_playing():
            yield (views.NewYear)
            yield (views.GrowthAndShock)
            if self.player.id_in_group < Constants.players_per_group:
                neighbour_id = self.player.id_in_group + 1
            else:
                neighbour_id = 1
            if self.player.num_playing == 1:
                yield (views.NoPlayersToRequest)
            elif self.player.num_playing == 2:
                if self.group.get_player_by_id(neighbour_id).dead_remove is not True:
                    yield (views.Request, {'request': True})
                    yield (views.RequestAmount, {'request_amount': 1})
                else:
                    yield (views.Request, {'request': False})
            elif self.player.num_playing > 2:
                if self.group.get_player_by_id(neighbour_id).dead_remove is not True:
                    yield (views.Request, {'request': True})
                    yield (views.RequestPlayer, {'request_player': neighbour_id})
                    yield (views.RequestAmount, {'request_amount': 1})
                else:
                    yield (views.Request, {'request': False})
            if self.player.num_playing > 1:
                if self.player.norequests:
                    yield (views.NoTransfers)
                else:
                    request_me = 0
                    others = self.player.get_others_in_group()
                    for o in others:
                        if o.request_player == self.player.id_in_group and o.request is True:
                            request_me += 1
                    if request_me > 0:
                        amount_sent = random.randint(0, self.participant.vars['herd_size'])
                        recipient = [p.id for p in self.player.sender.all()][0]
                        fulfill_dict = {
                            'sender-INITIAL_FORMS': (1, 1),
                            'sender-TOTAL_FORMS': (1, 1),
                            'sender-0-sender': self.player.pk,
                            'sender-0-id': recipient,
                            'sender-0-amount_sent': amount_sent,
                            }
                        yield (views.Fulfill, fulfill_dict)
                if not self.player.norequests:
                    yield (views.AllTransfers)
            assert self.participant.vars['herd_size'] >= 0
            yield (views.EndYear)
        if self.player.dead:
            yield (views.Dead)
        if self.player.round_number == Constants.num_rounds:
            yield Submission(views.EndExperiment, check_html=False)
