# Survival Game

Code written by Scott Claessens. Email: scott.claessens@hotmail.co.uk 

Please contact me if there are any issues.

<br>

## Summary

The Survival Game is an open-source experimental economic game, run on oTree. The game simulates the life of a Maasai pastoralist herder. In a live interaction, pairs of individuals manage herds of cattle. Their herds grow over time, but are also subject to unpredictable disasters, potentially reducing their herd size below a minimum ‘survival threshold’. Individuals must request help from their partner to survive.

<br>

## How to run the game

1) Install oTree.

- Visit http://otree.readthedocs.io/en/latest/install.html to learn how to install oTree. You may also need to install a recent version of Python. **IMPORTANT NOTE: This game will not work in oTree 2.0 or above.**

2) Run oTree in your computer's command line.

- Use ```cd``` in the command line to set the working directory as the folder this README.md is saved in.
- Run ```otree resetdb``` to reset the database.
- Run ```otree runserver``` to run a local server, in which you can demo the game locally.
- Access http://127.0.0.1:8000/demo/ to demo the game locally when the server is running.

3) To run an actual experiment, you will need to push the game online, rather than using the local server.

- The oTree docs give all the information on how to use Heroku (or other platforms) to push games
  online and run experiments.
- Be sure to cite oTree if you use this game to collect data! Citation: Chen, D.L., Schonger, M., Wickens, C., 2016. oTree - An open-source platform for laboratory, online and field experiments. Journal of Behavioral and Experimental Finance, vol 9: 88-97.


<br>

## Game schedule

1) **Herd births and deaths**. Each player's herd grows by a percentage, sampled from the Gaussian distribution specified by the parameters from session configs. Then, each player receives a shock ("disaster"), with a certain probability. The probability of shocks, the likelihood that they are correlated between ALL players, and the size (percentage reduction) of the shocks are all specified in the session configs.

2) **Request**. If there are other alive players to request from, players can request cattle from another player. Players must specify exactly how many cattle they want to request. If there is more than one other alive player, they must also specify exactly who they want to request from.

3) **Fulfill requests**. Players may fulfill the requests of others if they want. They are told how much a specific player is requesting, and can then give that player more / less than the requested amount, or nothing.

4) **End of year**. If there were cattle transfers, all players are informed of them. Then, the years ends. Final herd sizes are calculated, and if this falls beneath the minimum herd size threshold (specified in session configs), players are warned that they must increase it over the threshold or they run the risk of dying and being removed from the game. The amount of years, in a row, players can go with their herd under the minimum threshold is specified in the session configs.

<br>

## Game parameters (session configs)

The following game parameters can be edited before beginning an oTree session (default values used for demos).

```
NOTE: Default parameters are loosely based on the original model of need-based transfers, Aktipis, C. A., Cronk, L., & de Aguiar, R. (2011). Risk-pooling and herd survival: an agent-based model of a Maasai gift-giving system. Human Ecology, 39(2), 131-140. Locally-run demo versions of the game will automatically use default parameters.
```
```
NOTE2: 'Number of players per group' & 'number of rounds' are hard-coded "constants" in oTree, and so they cannot be edited as simply as the parameters below. In this demo, they are set to 2 and 10, respectively. To edit them, you will need to edit the code for the game directly:

   1. Go to SurvivalGame -> models.py
      - Edit "players_per_group" in Constants class
      - Edit "num_rounds" in Constants class
   2. Go to settings.py
      - Edit "num_demo_participants"
   3. You will need to then reset the database before playing the game: "otree resetdb"
```

| Parameter                              | Default (Range) | Description                                                  |
| :------------------------------------- | --------------- | ------------------------------------------------------------ |
| ```initialherd```                      | 70              | The number of cattle that players start the first year with. |
| ```minherd```                          | 64              | The minimum threshold for herd size. If a player's herd size goes BELOW this amount (equal is okay), they receive a warning and are told to increase it over the threshold. If they remain under the threshold for a certain number of years, they "die" and are removed from the game (see ```years_before_death```). |
| ```growth_rate_mean```                 | 0.034           | The mean of the Gaussian distribution from which growth rate is drawn. |
| ```growth_rate_sd```                   | 0.0253          | The standard deviation of the Gaussian distribution from which growth rate is drawn. |
| ```shock_rate```                       | 0.2 (0-1)       | The probability that a shock will occur on a given year. 0 = shocks do not occur. 1 = shocks occur every year. |
| ```shock_size_mean```                  | 0.15            | The mean of the Gaussian distribution from which shock size is drawn. |
| ```shock_size_sd```                    | 0.05            | The standard deviation of the Gaussian distribution from which shock size is drawn. |
| ```shock_correlated```                 | 0 (0-1)         | The probability that, if a shock occurs, it will affect all individuals identically (i.e. the same value is drawn from the Gaussian distribution for everyone). 0 = shocks are not correlated. 1 = shocks are correlated between all individuals (i.e. when a shock occurs, it affects all players identically). |
| ```shock_predictable```                | False (boolean) | If this is True, shocks cease to occur probabilistically, ind instead occur predictably, every *x* years (see ```shock_predictable_years```). Setting this to True bypasses both ```shock_rate``` and ```shock_correlated```, and instead determines the occurence of a shock by counting the number of years since the player's last one. |
| ```shock_predictable_years```          | 4               | This value is only important if ```shock_predictable``` is True. It states how often shocks occur (in years). Shock size is still calculated independently for each player, and shocks need not affect players simultaneously (i.e. the beginning of the 4-year cycle is random for each player). |
| ```years_before_death```               | 3               | How many years players can go (in a row) under the threshold before "dying" and being removed from the game. The first year a player *ends a year* under the threshold counts as the first year. |
| ```nonrandom_network_limited_degree``` | False (boolean) | Determines whether a constrained, limited network structure is imposed on groups. If this is set to False, players can request cattle from *any* other player (unless that player has died). If this is set to True, players can only interact with a limited number of neighbours (determined by ```nonrandom_network_k_degree```). This feature may be useful for very large groups. |
| ```nonrandom_network_k_degree```       | 4               | This value is only important if ```nonrandom_network_limited_degree``` is set to True. This value determines how many neighbours are included in each player's local network. This number *must* be between the group size and 2, and even numbers should be used (odd numbers necessarily lead to some one-way connections). |
| ```observability```                    | True (boolean)  | Determines whether players see the herd sizes of other players (and whether they are below the minimum threshold) on each screen as they play. |
| ```charts```                           | True (boolean)  | Determines whether players see a chart, visually displaying their current herd size on each screen. NOTE: HighCharts can slow pages down, so this may be worth deactivating. |
| ```summary_box```                      | False (boolean) | Determines whether players see a box summarising the requests during the year, on each screen. |
| ```real_world_currency_per_point```    | 0.01            | USD ($) per cattle, used to calculate bonus payment          |
| ```participation_fee```                | 1.00            | Base participation payment, in USD ($)                       |

<br>

## Dependent variables

```
NOTE: These are calculated for each player after they complete the game. The values are saved in the final round data.
```

| Dependent Variable                              | Description                                                  |
| ----------------------------------------------- | ------------------------------------------------------------ |
| ```rounds_survived```                           | The number of rounds the player survived.                    |
| ```overall_total_amount_requested```            | The total number of cattle the player requested.             |
| ```overall_total_amount_received```             | The total number of cattle the player received.              |
| ```overall_total_amount_given```                | The total number of cattle the player gave to others.        |
| ```overall_received_given_totaldiff```          | The difference between the total number of cattle the player gave to others, and the total number of cattle the player received from others. Negative number means the player gave more cattle than they received, across all rounds. |
| ```overall_mean_amount_requested```             | The mean number of cattle the player requested. Calculated by taking the ```overall_total_amount_requested``` and dividing by ```rounds_survived```. |
| ```overall_mean_amount_received```              | The mean number of cattle the player received. Calculated by taking the ```overall_total_amount_received``` and dividing by ```rounds_survived```. |
| ```overall_mean_amount_given```                 | The mean number of cattle the player gave to others. Calculated by taking the ```overall_total_amount_given``` and dividing by ```rounds_survived```. |
| ```overall_num_shocks```                        | The total number of shocks experienced.                      |
| ```overall_num_requests_made```                 | The total number of requests made.                           |
| ```overall_num_requests_when_under_threshold``` | The total number of requests that were made, specifically when the player's herd size was under the minimum threshold. |
| ```overall_num_requests_responded_to```         | The total number of others' requests the player responded to (i.e. the player gave at least 1 cattle). |
| ```overall_repetitive_giving```                 | When one player gives another player some cattle, the receiver becomes in "debt" to the sender. Giving cattle back to the sender removes the debt,  but pushes debt onto the original sender. If a player gives cattle to a player who is already in debt to them, this count of ```overall_repetitive_giving``` increments by 1. This variable can be thought of as: *the number of rounds in which the player sent cattle to someone who had not yet repaid a previous gift*. |
| ```overall_repetitive_asking```                 | If a player requests cattle from someone when they are already in debt to that person, this count of ```overall_repetitive_asking``` increments by 1. This variable could be thought of as: *the number of rounds in which the player requested cattle from someone when they had not yet repaid a previous gift from them*. |
