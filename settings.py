import os
from os import environ

import dj_database_url

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = ')nrkoaxxnu$37p@zep-&rs68m(3xo2(qebw*f%nk1xvp6x6ce_'

DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'cattle'


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
    'otree_mturk_utils',
    ]

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
oTree games
"""

mturk_hit_settings = {
    'keywords': ['psychology', 'bonus', 'decision', 'study', 'experiment'],
    'title': 'Group decision making',
    'description': 'A study about group decision making',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 45,
    'expiration_hours': 7*24,  # 7 days
    'grant_qualification_id': '39D9NJEN75PF1ZGLPH2SQGI07Y4HD6',
    'qualification_requirements': [
        # Location = US
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
        # Only workers who have not done my studies before
        {
            'QualificationTypeId': "39D9NJEN75PF1ZGLPH2SQGI07Y4HD6",
            'Comparator': "DoesNotExist",
        },
        # Number of hits approved > 50
        {
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThan",
            'IntegerValues': [50]
        },
        # HIT Approval Rate (%) for all Requesters' HITs
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThan",
            'IntegerValues': [97]
        },
    ],
}

# oTree Sentry. Should send emails with errors when not in DEBUG mode.

SENTRY_DSN = 'http://d606c64efb5d449d9ac450ef47fef1b0:1f312687dcc6423fa67a65d3b78782dc@sentry.otree.org/143'

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ROOM_DEFAULTS = {}

ROOMS = [
    {
        'name': 'HGP',
        'display_name': 'The Human Generosity Project - Conference Room',
        'participant_label_file': 'hgp_room.txt',
    },
    {
        'name': 'Evo_Psych_Class',
        'display_name': 'Intro to Evolutionary Psychology - Classroom',
        'participant_label_file': 'evo_psych_room.txt',
    },
]

SESSION_CONFIG_DEFAULTS = {
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
    'random_start_order': False,
}


SESSION_CONFIGS = [
    {
        'name': 'SurvivalGame_Visible',
        'display_name': 'Survival Game - Visible',
        'num_demo_participants': 2,
        'app_sequence': [
            'Demographics',
            'Instructions',
            'ExampleYear',
            'Comprehension',
            'SurvivalGame',
            'Earnings',
            'Feedback',
        ],

        # For descriptions of each of these, see README - Survival Game.txt
        #
        'initialherd': 70,                          # 70
        'minherd': 64,                              # 64
        'growth_rate_mean': 0.034,                  # 0.034
        'growth_rate_sd': 0.0253,                   # 0.0253
        'shock_rate': 0.2,                          # 0.1
        'shock_size_mean': 0.15,                    # 0.3
        'shock_size_sd': 0.05,                      # 0.1
        'shock_correlated': 0,                      # 0
        'shock_predictable': False,                 # False
        'shock_predictable_years': 4,               # 4
        'years_before_death': 3,                    # 3
        'nonrandom_network_limited_degree': False,  # False
        'nonrandom_network_k_degree': 4,            # 4
        'visible_ask': True,                        # True
        'visible_give': True,                       # True
        'charts': True,                             # True
        'summary_box': False,                       # False
        'real_world_currency_per_point': 0.01,      # 0.01
        'participation_fee': 3.50,                  # 1.00
    },
    {
        'name': 'SurvivalGame_VisibleWhenAsk',
        'display_name': 'Survival Game - Visible (Only when asking)',
        'num_demo_participants': 2,
        'app_sequence': [
            'Demographics',
            'Instructions',
            'ExampleYear',
            'Comprehension',
            'SurvivalGame',
            'Earnings',
            'Feedback',
        ],

        # For descriptions of each of these, see README - Survival Game.txt
        #
        'initialherd': 70,                          # 70
        'minherd': 64,                              # 64
        'growth_rate_mean': 0.034,                  # 0.034
        'growth_rate_sd': 0.0253,                   # 0.0253
        'shock_rate': 0.2,                          # 0.1
        'shock_size_mean': 0.15,                    # 0.3
        'shock_size_sd': 0.05,                      # 0.1
        'shock_correlated': 0,                      # 0
        'shock_predictable': False,                 # False
        'shock_predictable_years': 4,               # 4
        'years_before_death': 3,                    # 3
        'nonrandom_network_limited_degree': False,  # False
        'nonrandom_network_k_degree': 4,            # 4
        'visible_ask': True,                        # True
        'visible_give': False,                      # True
        'charts': True,                             # True
        'summary_box': False,                       # False
        'real_world_currency_per_point': 0.01,      # 0.01
        'participation_fee': 3.50,                  # 1.00
    },
    {
        'name': 'SurvivalGame_VisibleWhenGive',
        'display_name': 'Survival Game - Visible (Only when giving)',
        'num_demo_participants': 2,
        'app_sequence': [
            'Demographics',
            'Instructions',
            'ExampleYear',
            'Comprehension',
            'SurvivalGame',
            'Earnings',
            'Feedback',
        ],

        # For descriptions of each of these, see README - Survival Game.txt
        #
        'initialherd': 70,                          # 70
        'minherd': 64,                              # 64
        'growth_rate_mean': 0.034,                  # 0.034
        'growth_rate_sd': 0.0253,                   # 0.0253
        'shock_rate': 0.2,                          # 0.1
        'shock_size_mean': 0.15,                    # 0.3
        'shock_size_sd': 0.05,                      # 0.1
        'shock_correlated': 0,                      # 0
        'shock_predictable': False,                 # False
        'shock_predictable_years': 4,               # 4
        'years_before_death': 3,                    # 3
        'nonrandom_network_limited_degree': False,  # False
        'nonrandom_network_k_degree': 4,            # 4
        'visible_ask': False,                       # True
        'visible_give': True,                       # True
        'charts': True,                             # True
        'summary_box': False,                       # False
        'real_world_currency_per_point': 0.01,      # 0.01
        'participation_fee': 3.50,                  # 1.00
    },
    {
        'name': 'SurvivalGame_Hidden',
        'display_name': 'Survival Game - Hidden',
        'num_demo_participants': 2,
        'app_sequence': [
            'Demographics',
            'Instructions',
            'ExampleYear',
            'Comprehension',
            'SurvivalGame',
            'Earnings',
            'Feedback',
        ],

        # For descriptions of each of these, see README - Survival Game.txt
        #
        'initialherd': 70,                          # 70
        'minherd': 64,                              # 64
        'growth_rate_mean': 0.034,                  # 0.034
        'growth_rate_sd': 0.0253,                   # 0.0253
        'shock_rate': 0.2,                          # 0.1
        'shock_size_mean': 0.15,                    # 0.3
        'shock_size_sd': 0.05,                      # 0.1
        'shock_correlated': 0,                      # 0
        'shock_predictable': False,                 # False
        'shock_predictable_years': 4,               # 4
        'years_before_death': 3,                    # 3
        'nonrandom_network_limited_degree': False,  # False
        'nonrandom_network_k_degree': 4,            # 4
        'visible_ask': False,                       # True
        'visible_give': False,                      # True
        'charts': True,                             # True
        'summary_box': False,                       # False
        'real_world_currency_per_point': 0.01,      # 0.01
        'participation_fee': 3.50,                  # 1.00
    },
]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
