from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from otree.models_concrete import PageCompletion
from django.db import models as djmodels
from django.db.models import Q, Sum

author = 'Scott Claessens'

doc = """Survival Game"""


class Constants(BaseConstants):
    name_in_url = 'SurvivalGame'
    players_per_group = 2
    num_rounds = 25


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        #
        # This code specifies the information shown on the oTree admin page.
        # Each transfer of cattle is displayed in the admin report.
        #
        aps = self.get_players()
        all_transfers = SendReceive.objects.filter(Q(sender__in=aps) | Q(receiver__in=aps)).values(
            'sender__id_in_group',
            'receiver__id_in_group',
            'amount_sent',
            'amount_requested',
            'sender__group__id_in_subsession')

        return {'all_transfers': all_transfers}

    def creating_session(self):
        #
        # When the session is created, these initial 'participant variables' are created for every participant
        #
        for p in self.get_players():
            p.participant.vars['go_to_the_end'] = False
            # initially go_to_the_end = False, but will be set to True if participant abandons game

            p.participant.vars['waiting_time_lobby'] = 0
            # time spent waiting in the lobby goes here

            p.participant.vars['payment_for_wait'] = 0
            # payment_for_wait is amount paid for waiting in the lobby

            p.participant.vars['payment_for_game'] = 0
            # payment from the game itself goes here

            p.participant.vars['herd_size'] = c(self.session.config['initialherd'])
            # herd_size variable holds the participant's current herd size

            p.participant.vars['total_cattle_lost'] = 0
            # count of number of cattle lost to disasters (shocks) across all years

            p.participant.vars['under_minimum_years_left'] = self.session.config['years_before_death']
            # under_minimum_years_left decreases every year the player is under the minimum threshold

            p.participant.vars['dead'] = False
            # this is set to True when a player dies, and they are removed from the game

            p.participant.vars['debt'] = []
            # this variable is used to calculate repetitive giving and asking

            p.participant.vars['repetitive_giving'] = 0
            # this counter goes up every time the player gives to another player without being reciprocated

            p.participant.vars['repetitive_asking'] = 0
            # this count goes up every time the player asks for cattle from a player they have yet to reciprocate to

            p.participant.vars['others_in_network'] = []
            # a list of all the players in the participant's 'network'
            # (more relevant when nonrandom_network_limited_degree = True)

            p.participant.vars['shock_predictable_yearcount'] = random.randint(
                1, self.session.config['shock_predictable_years'])
            # when shocks occur every x years, this sets the initial 'year count cycle' at 1 <= yearcount <= x
            # then when yearcount = x, a shock occurs


class Group(BaseGroup):
    def create_group(self):
        #
        # Code runs after group is formed in the waiting lobby
        #
        for p in self.get_players():
            # If networks are being used, calculate 'neighbours' and add them to others_in_network list
            if self.session.config['nonrandom_network_limited_degree']:
                n = 0
                k = 1
                while n < self.session.config['nonrandom_network_k_degree']:
                    n += 1
                    if n % 2 == 0:
                        if p.id_in_group - k <= 0:
                            p.participant.vars['others_in_network'].append(
                                Constants.players_per_group + p.id_in_group - k)
                        else:
                            p.participant.vars['others_in_network'].append(
                                p.id_in_group - k)
                        k += 1
                    else:
                        if p.id_in_group + k > Constants.players_per_group:
                            p.participant.vars['others_in_network'].append(
                                p.id_in_group + k - Constants.players_per_group)
                        else:
                            p.participant.vars['others_in_network'].append(
                                p.id_in_group + k)
                p.participant.vars['others_in_network'].sort()
            # Else if networks are not being used, whole group added to others_in_network list
            else:
                for o in p.get_others_in_group():
                    p.participant.vars['others_in_network'].append(o.id_in_group)
                p.participant.vars['others_in_network'].sort()

    def set_shock(self):
        #
        # Code runs in the wait page before GrowthAndShocks page
        #
        if self.session.config['shock_predictable']:
            # If shocks are predictable...
            for p in self.get_players():
                # Increment year count
                if p.participant.vars['shock_predictable_yearcount'] < self.session.config[
                                                                            'shock_predictable_years']:
                    p.participant.vars['shock_predictable_yearcount'] += 1
                else:
                    p.participant.vars['shock_predictable_yearcount'] = 1
                if p.dead_remove is not True:
                    # If yearcount aligns with frequency of shocks, shock occurs
                    if p.participant.vars['shock_predictable_yearcount'] == self.session.config[
                                                                            'shock_predictable_years']:
                        p.shock_occurrence = True
                        # calculate size of shock
                        shock_size = random.gauss(
                            self.session.config['shock_size_mean'], self.session.config['shock_size_sd'])
                        # increment count of total_cattle_lost
                        p.participant.vars['total_cattle_lost'] += shock_size * p.participant.vars['herd_size']
                        # reduce herd size by that amount
                        p.participant.vars['herd_size'] = \
                            p.participant.vars['herd_size'] - (shock_size * p.participant.vars['herd_size'])
                    else:
                        p.shock_occurrence = False
        else:
            # If shocks should be uncorrelated...
            if random.uniform(0, 1) > self.session.config['shock_correlated']:
                # shock occurrence / severity calculated independently for each player
                for p in self.get_players():
                    if p.dead_remove is not True:
                        if random.uniform(0, 1) < self.session.config['shock_rate']:
                            p.shock_occurrence = True
                            # calculate size of shock
                            shock_size = random.gauss(
                                self.session.config['shock_size_mean'], self.session.config['shock_size_sd'])
                            # increment count of total_cattle_lost
                            p.participant.vars['total_cattle_lost'] += shock_size * p.participant.vars['herd_size']
                            # reduce herd size by that amount
                            p.participant.vars['herd_size'] = \
                                p.participant.vars['herd_size'] - (shock_size * p.participant.vars['herd_size'])
                        else:
                            p.shock_occurrence = False
            # If shocks should be correlated...
            else:
                # shock occurrence / severity calculated for group as a whole
                if random.uniform(0, 1) < self.session.config['shock_rate']:
                    # calculate size of shock
                    shock_size = random.gauss(self.session.config['shock_size_mean'], self.session.config['shock_size_sd'])
                    for p in self.get_players():
                        if p.dead_remove is not True:
                            p.shock_occurrence = True
                            # increment count of total_cattle_lost
                            p.participant.vars['total_cattle_lost'] += shock_size * p.participant.vars['herd_size']
                            # reduce herd size by that amount
                            p.participant.vars['herd_size'] = \
                                p.participant.vars['herd_size'] - (shock_size * p.participant.vars['herd_size'])
                else:
                    for p in self.get_players():
                        if p.dead_remove is not True:
                            p.shock_occurrence = False
        # finally, set herd_size_after_shock and under_minimum for each player
        for p in self.get_players():
            if p.dead_remove is not True:
                if p.participant.vars['herd_size'] <= c(0):
                    p.participant.vars['herd_size'] = c(0)
                p.herd_size_after_shock = p.participant.vars['herd_size']
                if p.herd_size_after_shock < c(self.session.config['minherd']):
                    p.under_minimum = True
                else:
                    p.under_minimum = False

    def no_requests(self):
        #
        # Code runs in the wait page after Request page
        #
        # set norequests, depending on whether anyone in my network requested cattle this year
        for p in self.get_players():
            n = 0
            network = p.participant.vars['others_in_network'] + [p.id_in_group]
            for o in network:
                q = self.get_player_by_id(o)
                if q.request is True:
                    n += 1
            if n == 0:
                p.norequests = True
            else:
                p.norequests = False

    def outgoing(self):
        #
        # Code runs in the wait page after Fulfill / NoTransfers
        #
        # calculate amount of cattle outgoing for each player
        for p in self.get_players():
            tot_sent = (p.sender.aggregate(tot_sent=Sum('amount_sent'))['tot_sent'] or 0)
            p.participant.vars['herd_size'] -= tot_sent

    def incoming(self):
        #
        # Code runs in the wait page after Fulfill / NoTransfers
        #
        # calculate amount of cattle incoming for each player
        for p in self.get_players():
            tot_received = (p.receiver.aggregate(tot_received=Sum('amount_sent'))['tot_received'] or 0)
            p.participant.vars['herd_size'] += tot_received
            if p.request:
                p.received = tot_received

    def debts(self):
        #
        # Code runs in the wait page after Fulfill / NoTransfers
        #
        # 1) calculate repetitive asking / giving
        # 2) calculate new debts
        # 3) remove satisfied debts
        for p in self.get_players():
            # if I requested from another player, check if I'm already in debt to that player
            # if I am in debt, count repetitive asking
            if p.request and p.request_player in p.participant.vars['debt']:
                p.participant.vars['repetitive_asking'] += 1
            # if I fulfilled another player's request (positively), check if they are already in debt to me
            # if they are, count repetitive giving
            for o in p.get_others_in_group():
                if o.request and o.request_player == p.id_in_group and o.received > 0:
                    if p.id_in_group in o.participant.vars['debt']:
                        p.participant.vars['repetitive_giving'] += 1
        for p in self.get_players():
            # if another player fulfilled my request (positive), check if I'm already in debt to that player
            # if I'm not, add them to my debt list
            if p.request and p.received > 0:
                if p.request_player not in p.participant.vars['debt']:
                    p.participant.vars['debt'].append(p.request_player)
            # if I fulfilled another player's request (positively), check if I'm already in debt to that player
            # if I am, remove debt
            for o in p.get_others_in_group():
                if o.request and o.request_player == p.id_in_group and o.received > 0:
                    if o.id_in_group in p.participant.vars['debt']:
                        p.participant.vars['debt'].remove(o.id_in_group)

    def final_herd_size(self):
        #
        # Code runs in the wait page after Fulfill / NoTransfers
        #
        # set herd_size_after_transfers, under_minimum and dead
        for n in self.get_players():
            if n.participant.vars['herd_size'] <= c(0):
                n.participant.vars['herd_size'] = c(0)
            if n.dead_remove is not True:
                n.herd_size_after_transfers = c(n.participant.vars['herd_size'])
                if n.herd_size_after_transfers < c(self.session.config['minherd']):
                    n.under_minimum = True
                    n.participant.vars['under_minimum_years_left'] -= 1
                else:
                    n.under_minimum = False
                    n.participant.vars['under_minimum_years_left'] = self.session.config['years_before_death']
                n.under_minimum_years_left_end = n.participant.vars['under_minimum_years_left']
                if n.under_minimum_years_left_end == 0:
                    n.dead = True
                else:
                    n.dead = False


class Player(BasePlayer):
    def set_under_minimum_years_left(self):
        #
        # Code runs after NewYear
        #
        # set variable under_minimum_years_left
        self.under_minimum_years_left = self.participant.vars['under_minimum_years_left']

    def set_num_playing(self):
        #
        # Code runs after NewYear
        #
        # set variable num_playing (number of players in my network still alive)
        n = 0
        if self.session.config['nonrandom_network_limited_degree']:
            for o in self.participant.vars['others_in_network']:
                p = self.group.get_player_by_id(o)
                if p.dead_remove:
                    n += 1
            self.num_playing = len(self.participant.vars['others_in_network']) - n + 1
        else:
            for o in self.get_others_in_group():
                if o.dead_remove:
                    n += 1
            self.num_playing = Constants.players_per_group - n

    def set_growth(self):
        #
        # Code runs after NewYear
        #
        # calculate growth independently for each player, add to herd_size, set herd_size_after growth and under_minimum
        if self.dead_remove is not True:
            self.herd_size_initial = self.participant.vars['herd_size']
            growth_rate = random.gauss(self.session.config['growth_rate_mean'], self.session.config['growth_rate_sd'])
            self.participant.vars['herd_size'] = \
                self.participant.vars['herd_size'] + (growth_rate * self.participant.vars['herd_size'])
            if self.participant.vars['herd_size'] <= c(0):
                self.participant.vars['herd_size'] = c(0)
            self.herd_size_after_growth = self.participant.vars['herd_size']
            if self.herd_size_after_growth < c(self.session.config['minherd']):
                self.under_minimum = True
            else:
                self.under_minimum = False

    def set_request_player(self):
        #
        # Code runs after Request page
        #
        # if there are only two players left alive in my network, choose the other player as requestee automatically
        if self.num_playing == 2 and self.request:
            for o in self.participant.vars['others_in_network']:
                p = self.group.get_player_by_id(o)
                if p.dead_remove is not True:
                    self.request_player = p.id_in_group

    def set_dead(self):
        #
        # Code runs after End of Year page
        #
        # sets dead variable
        if self.dead:
            self.participant.vars['dead'] = True

    def set_remove_from_game(self):
        #
        # Code runs after End of Year page, if player is dead
        #
        # sets dead_remove, to remove the dead player from the rest of the game
        for n in range(1, Constants.num_rounds+1):
            if self.in_round(n).dead is None:
                self.in_round(n).dead_remove = True
        self.in_round(Constants.num_rounds).rounds_survived = self.round_number

    def set_payoff_and_dvs(self):
        #
        # Code runs after the experiment is completed, either by normal completion, death, or game abandonment
        #
        # Set payment_for_wait
        self.participant.vars['waiting_time_lobby'] += sum(PageCompletion.objects.filter(
            participant=self.participant,
            page_name__in=['GroupingWait']).values_list(
            'seconds_on_page',
            flat=True))
        self.participant.vars['payment_for_wait'] += \
            self.participant.vars['waiting_time_lobby'] * (5/60)  # seconds multiplied into points for payment

        # Set max payment from waiting lobby to $0.50 (ten minutes of waiting) and round to integer
        if self.participant.vars['payment_for_wait'] > 50:
            self.participant.vars['payment_for_wait'] = 50
        self.participant.vars['payment_for_wait'] = int(round(self.participant.vars['payment_for_wait']))

        # Record payment from the waiting lobby, and add it to payoffs
        self.in_round(Constants.num_rounds).payment_for_lobby = self.participant.vars['payment_for_wait']
        self.participant.payoff += c(self.participant.vars['payment_for_wait'])

        # Record payment from game
        self.participant.vars['payment_from_game'] = int(round(sum(filter(None,
            [p.herd_size_initial for p in self.in_all_rounds()]))) / 10)

        # Set max payment from game to $10.00
        if self.participant.vars['payment_from_game'] > 1000:
            self.participant.vars['payment_from_game'] = 1000

        # Add payment from game to payoffs
        self.in_round(Constants.num_rounds).payment_from_game = self.participant.vars['payment_from_game']
        self.participant.payoff += self.participant.vars['payment_from_game']

        # Record whether group dropped out (game abandoned)
        if any([p.participant.vars['go_to_the_end'] for p in self.group.get_players()]):
            self.in_round(Constants.num_rounds).game_abandoned = True
        else:
            self.in_round(Constants.num_rounds).game_abandoned = False

        # Record total amount of cattle lost
        self.in_round(Constants.num_rounds).total_cattle_lost = self.participant.vars['total_cattle_lost']

        # Calculate other DVs (these calculations go into the final round, for ease of viewing)
        n = 0
        for r in range(1, Constants.num_rounds+1):
            if self.in_round(r).dead_remove is not True:
                n += 1
        self.in_round(Constants.num_rounds).overall_total_amount_requested = sum(filter(None,
                                                                                        [p.request_amount for p in
                                                                                         self.in_all_rounds()]))
        self.in_round(Constants.num_rounds).overall_total_amount_given = sum(filter(None,
                                                                                    [(p.sender.aggregate(
                                                                                        tot_sent=Sum(
                                                                                            'amount_sent'))[
                                                                                          'tot_sent'] or 0) for p in
                                                                                     self.in_all_rounds()]))
        self.in_round(Constants.num_rounds).overall_total_amount_received = sum(filter(None,
                                                                                [(p.receiver.aggregate(
                                                                                    tot_sent=Sum(
                                                                                        'amount_sent'))[
                                                                                      'tot_sent'] or 0) for p in
                                                                                 self.in_all_rounds()]))
        self.in_round(Constants.num_rounds).overall_received_given_totaldiff = \
            self.in_round(Constants.num_rounds).overall_total_amount_received - \
            self.in_round(Constants.num_rounds).overall_total_amount_given
        self.in_round(Constants.num_rounds).overall_mean_amount_requested = float(sum(filter(None,
                                                                                [p.request_amount for p in
                                                                                 self.in_all_rounds()]))) / float(n)
        self.in_round(Constants.num_rounds).overall_mean_amount_received = sum(filter(None,
                                                                               [(p.receiver.aggregate(
                                                                                   tot_sent=Sum('amount_sent'))[
                                                                                     'tot_sent'] or 0) for p in
                                                                                self.in_all_rounds()])) / float(n)
        self.in_round(Constants.num_rounds).overall_mean_amount_given = sum(filter(None,
                                                                            [(p.sender.aggregate(
                                                                                tot_sent=Sum('amount_sent'))[
                                                                                  'tot_sent'] or 0) for p in
                                                                             self.in_all_rounds()])) / float(n)
        a = 0
        b = 0
        d = 0
        for r in range(1, Constants.num_rounds+1):
            if self.in_round(r).shock_occurrence:
                d += 1
            if self.in_round(r).request:
                a += 1
                if self.in_round(r).herd_size_after_shock < c(self.session.config['minherd']):
                    b += 1
        self.in_round(Constants.num_rounds).overall_num_shocks = d
        self.in_round(Constants.num_rounds).overall_num_requests_made = a
        self.in_round(Constants.num_rounds).overall_num_requests_when_under_threshold = b
        self.in_round(Constants.num_rounds).overall_num_requests_responded_to = sum(filter(None,
            [(p.sender.filter(amount_sent__gt=0).count()) for p in self.in_all_rounds()]))
        self.in_round(Constants.num_rounds).overall_repetitive_giving = self.participant.vars['repetitive_giving']
        self.in_round(Constants.num_rounds).overall_repetitive_asking = self.participant.vars['repetitive_asking']

    def is_playing(self):
        return self.participant.vars['dead'] is False

    under_minimum_years_left = models.PositiveIntegerField()

    num_playing = models.PositiveIntegerField(initial=0)

    herd_size_initial = models.CurrencyField()

    herd_size_after_growth = models.CurrencyField()

    shock_occurrence = models.BooleanField()

    herd_size_after_shock = models.CurrencyField()

    request = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No'],
                 ],
        widget=widgets.RadioSelect(),
        verbose_name="Would you like to ask for cattle from the other player?"
    )

    request_player = models.IntegerField(
        widget=widgets.RadioSelect,
        verbose_name="Which player would you like to ask for cattle from?"
    )

    request_amount = models.CurrencyField(
        min=c(1),
        verbose_name="How many cattle would you like to ask this player for?"
    )

    sr_dump = models.CharField()

    received = models.CurrencyField()

    norequests = models.BooleanField()

    herd_size_after_transfers = models.CurrencyField()

    under_minimum_years_left_end = models.PositiveIntegerField()

    under_minimum = models.BooleanField()

    dead = models.BooleanField()

    dead_remove = models.BooleanField()

    rounds_survived = models.IntegerField()

    total_cattle_lost = models.IntegerField()

    overall_total_amount_requested = models.CurrencyField()

    overall_total_amount_received = models.CurrencyField()

    overall_total_amount_given = models.CurrencyField()

    overall_received_given_totaldiff = models.CurrencyField()

    overall_mean_amount_requested = models.FloatField()

    overall_mean_amount_received = models.FloatField()

    overall_mean_amount_given = models.FloatField()

    overall_num_shocks = models.IntegerField()

    overall_num_requests_made = models.IntegerField()

    overall_num_requests_when_under_threshold = models.IntegerField()

    overall_num_requests_responded_to = models.IntegerField()

    overall_repetitive_giving = models.IntegerField()

    overall_repetitive_asking = models.IntegerField()

    payment_for_lobby = models.IntegerField()

    payment_from_game = models.IntegerField()

    game_abandoned = models.BooleanField()


class SendReceive(djmodels.Model):
    receiver = djmodels.ForeignKey(Player, related_name='receiver')
    sender = djmodels.ForeignKey(Player, related_name='sender')
    amount_requested = models.IntegerField()
    amount_sent = models.IntegerField(blank=True)
