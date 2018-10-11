from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, Player, SendReceive
import django
from django import forms
from .forms import SRFormSet
from django.db.models import Q
from otree_mturk_utils.views import CustomMturkPage, CustomMturkWaitPage


def vars_for_all_templates(self):
    other_players = []
    for o in self.player.participant.vars['others_in_network']:
        p = self.group.get_player_by_id(o)
        other_players.append(p)
    return {'herd_size_for_chart': int(self.player.participant.vars['herd_size']),
            'visible_ask': self.session.config['visible_ask'],
            'visible_give': self.session.config['visible_give'],
            'round_number': self.subsession.round_number,
            'minherd': self.session.config['minherd'],
            'charts': self.session.config['charts'],
            'summary_box': self.session.config['summary_box'],
            'others_in_network': self.player.participant.vars['others_in_network'],
            'other_players': other_players,
            'limited_degree': self.session.config['nonrandom_network_limited_degree'],
            'k': self.session.config['nonrandom_network_k_degree'],
            'go_to_the_end': self.player.participant.vars['go_to_the_end'],
            }


class GroupingWait(CustomMturkWaitPage):
    group_by_arrival_time = True
    # should an effort task be included in the waiting lobby page?
    use_task = True
    # when should the timer on the waiting lobby page start (in seconds)?
    startwp_timer = 600

    def is_displayed(self):
        return self.round_number == 1

    def after_all_players_arrive(self):
        self.group.create_group()


class PlayingPage(CustomMturkPage):
    #
    # Page only shown if player is_playing (i.e. is still alive) and has not abandoned the game yet
    #
    def is_displayed(self):
        return self.player.is_playing() and not self.player.participant.vars['go_to_the_end']

    # this generalises go_to_the_end to every member of group, immediately
    def before_next_page(self):
        if any([p.participant.vars.get('go_to_the_end') for p in self.group.get_players()]):
            self.player.participant.vars['go_to_the_end'] = True

    # how long should the 'fake' timer count down for?
    timeout_seconds = 90


class PlayingWaitPage(CustomMturkWaitPage):
    # no task on normal wait pages
    use_task = False
    # length of timer on normal wait pages
    startwp_timer = 90

    def is_displayed(self):
        return self.player.is_playing() and not self.participant.vars['go_to_the_end']

    def after_all_players_arrive(self):
        # this generalises go_to_the_end to every member of group, immediately
        if any([p.participant.vars.get('go_to_the_end') for p in self.group.get_players()]):
            for p in self.group.get_players():
                p.participant.vars['go_to_the_end'] = True


class Wait(PlayingWaitPage):
    pass


class Initial(PlayingPage):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'initial': self.session.config['initialherd']
                }


class NewYear(PlayingPage):
    def before_next_page(self):
        self.player.set_growth()
        self.player.set_num_playing()
        self.player.set_under_minimum_years_left()


class ShockWait(PlayingWaitPage):
    def after_all_players_arrive(self):
        self.group.set_shock()


class GrowthAndShock(PlayingPage):
    def vars_for_template(self):
        return {'under_minimum': self.player.under_minimum,
                'under_minimum_years_left': self.player.under_minimum_years_left,
                'herd_size_initial': self.player.herd_size_initial,
                'herd_size_after_growth': self.player.herd_size_after_growth,
                'herd_size_after_shock': self.player.herd_size_after_shock,
                'shock_occurrence': self.player.shock_occurrence,
                'num_players': self.player.num_playing,
                'dead_remove': self.player.dead_remove
                }


class NoPlayersToRequest(PlayingPage):
    def is_displayed(self):
        return self.player.num_playing == 1

    def vars_for_template(self):
        return {'herd_size_after_shock': self.player.herd_size_after_shock}


class Request(PlayingPage):
    form_model = models.Player
    form_fields = ['request']

    def is_displayed(self):
        return self.player.num_playing > 1

    def vars_for_template(self):
        return {'under_minimum': self.player.under_minimum,
                'under_minimum_years_left': self.player.under_minimum_years_left,
                'herd_size_after_shock': self.player.herd_size_after_shock,
                'num_players': self.player.num_playing,
                'dead_remove': self.player.dead_remove
                }

    def before_next_page(self):
        return self.player.set_request_player()


class RequestsWait(PlayingWaitPage):
    def is_displayed(self):
        return self.player.num_playing > 1

    def after_all_players_arrive(self):
        self.group.no_requests()


class RequestPlayer(PlayingPage):
    def is_displayed(self):
        return self.player.request and self.player.num_playing > 2

    form_model = models.Player
    form_fields = ['request_player']

    def request_player_choices(self):
        choices = []
        if self.session.config['nonrandom_network_limited_degree']:
            for o in self.player.participant.vars['others_in_network']:
                p = self.group.get_player_by_id(o)
                if p.dead_remove is not True:
                    choices.append((p.id_in_group, "Player {}".format(p.id_in_group)))
        else:
            for o in self.player.get_others_in_group():
                if o.dead_remove is not True:
                    choices.append((o.id_in_group, "Player {}".format(o.id_in_group)))
        return choices

    def vars_for_template(self):
        return {'under_minimum': self.player.under_minimum,
                'under_minimum_years_left': self.player.under_minimum_years_left,
                'herd_size_after_shock': self.player.herd_size_after_shock,
                'dead_remove': self.player.dead_remove,
                }


class RequestAmount(PlayingPage):
    form_model = models.Player
    form_fields = ['request_amount']

    def is_displayed(self):
        return self.player.request and self.player.num_playing > 1

    def vars_for_template(self):
        return {'under_minimum': self.player.under_minimum,
                'under_minimum_years_left': self.player.under_minimum_years_left,
                'herd_size_after_shock': self.player.herd_size_after_shock,
                'request': self.player.request,
                'request_player': self.player.request_player,
                'num_players': self.player.num_playing,
                'dead_remove': self.player.dead_remove,
                }

    def before_next_page(self):
        if self.player.request:
            target = Player.objects.get(id_in_group=self.player.request_player,
                                        subsession=self.subsession, group=self.group)
            sr, created = self.player.receiver.get_or_create(sender=target,
                                                             defaults={'amount_requested': self.player.request_amount})
            sr.save()


class Fulfill(PlayingPage):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = SRFormSet(instance=self.player)
        return context

    def post(self):
        context = super().get_context_data()
        formset = SRFormSet(self.request.POST, instance=self.player)
        context['formset'] = formset
        if not formset.is_valid():
            return self.render_to_response(context)
        formset.save()
        return super().post()

    def before_next_page(self):
        to_dump_sender = self.player.sender.values('receiver__id_in_group', 'amount_sent', 'amount_requested', )
        to_dump_receiver = self.player.receiver.values('sender__id_in_group', 'amount_sent', 'amount_requested', )
        self.player.sr_dump = {'sending': to_dump_sender,
                               'receiving': to_dump_receiver}

    def vars_for_template(self):
        request_me = 0
        others = self.player.get_others_in_group()
        for o in others:
            if o.request_player == self.player.id_in_group:
                request_me += 1
        return {'request_me': request_me,
                'under_minimum': self.player.under_minimum,
                'under_minimum_years_left': self.player.under_minimum_years_left,
                'herd_size_after_shock': self.player.herd_size_after_shock,
                'request': self.player.request,
                'request_player': self.player.request_player,
                'request_amount': self.player.request_amount,
                'num_players': self.player.num_playing,
                'dead_remove': self.player.dead_remove,
                }

    def is_displayed(self):
        request_me = 0
        others = self.player.get_others_in_group()
        for o in others:
            if o.request_player == self.player.id_in_group and o.request is True:
                request_me += 1
        return self.player.norequests is False and request_me > 0


class NoTransfers(PlayingPage):
    def is_displayed(self):
        return self.player.num_playing > 1 and self.player.norequests

    def vars_for_template(self):
        return {'herd_size_after_shock': self.player.herd_size_after_shock,
                }


class TransferWait(PlayingWaitPage):
    def after_all_players_arrive(self):
        self.group.incoming()
        self.group.outgoing()
        self.group.debts()
        self.group.final_herd_size()


class AllTransfers(PlayingPage):
    def vars_for_template(self):
        network = []
        for o in self.player.participant.vars['others_in_network']:
            p = self.group.get_player_by_id(o)
            if p.dead_remove is not True:
                network.append(p)
        network = [self.group.get_player_by_id(self.player.id_in_group)] + network
        all_transfers = \
            SendReceive.objects.filter(Q(sender__in=network) | Q(receiver__in=network)).values('sender__id_in_group',
                                                                                               'receiver__id_in_group',
                                                                                               'amount_sent')
        print(all_transfers)
        request_me = 0
        others = self.player.get_others_in_group()
        for o in others:
            if o.request_player == self.player.id_in_group:
                request_me += 1
        return {'request_me': request_me,
                'all_transfers': all_transfers,
                'herd_size_after_transfers': self.player.herd_size_after_transfers,
                'request': self.player.request,
                'request_player': self.player.request_player,
                'request_amount': self.player.request_amount
                }

    def is_displayed(self):
        return self.player.num_playing > 1 and not self.player.norequests


class EndYear(PlayingPage):
    def vars_for_template(self):
        network = []
        for o in self.player.participant.vars['others_in_network']:
            p = self.group.get_player_by_id(o)
            if p.dead_remove is not True:
                network.append(p)
        network = [self.group.get_player_by_id(self.player.id_in_group)] + network
        all_transfers = SendReceive.objects.filter(Q(sender__in=network) | Q(receiver__in=network)).values(
            'sender__id_in_group',
            'receiver__id_in_group',
            'amount_sent')
        print(all_transfers)
        request_me = 0
        others = self.player.get_others_in_group()
        for o in others:
            if o.request_player == self.player.id_in_group:
                request_me += 1
        return {'request_me': request_me,
                'all_transfers': all_transfers,
                'herd_size_after_transfers': self.player.herd_size_after_transfers,
                'under_minimum': self.player.under_minimum,
                'under_minimum_years_left_end': self.player.under_minimum_years_left_end,
                'under_minimum_years_before_death': self.session.config['years_before_death'],
                'dead': self.player.dead,
                'num_players': self.player.num_playing,
                'dead_remove': self.player.dead_remove,
                'request': self.player.request,
                'request_player': self.player.request_player,
                'request_amount': self.player.request_amount,
                'repetitive_asking': self.participant.vars['repetitive_asking'],
                'repetitive_giving': self.participant.vars['repetitive_giving'],
                'debt': self.participant.vars['debt']
                }

    def before_next_page(self):
        self.player.set_dead()
        if self.player.dead:
            self.player.set_remove_from_game()
        elif self.player.dead is not True and self.round_number == Constants.num_rounds:
            self.player.in_round(Constants.num_rounds).rounds_survived = Constants.num_rounds


class Dead(CustomMturkPage):
    def is_displayed(self):
        return self.player.dead


class MTurkFinish(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds and self.player.participant.vars['go_to_the_end']


class EndExperiment(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.set_payoff_and_dvs()


page_sequence = [
    GroupingWait,
    Initial,
    NewYear,
    ShockWait,
    GrowthAndShock,
    NoPlayersToRequest,
    Wait,
    Request,
    RequestsWait,
    RequestPlayer,
    RequestAmount,
    Wait,
    Fulfill,
    Wait,
    NoTransfers,
    TransferWait,
    AllTransfers,
    EndYear,
    Dead,
    Wait,
    MTurkFinish,
    EndExperiment
]
