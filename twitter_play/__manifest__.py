# -*- coding: utf-8 -*-
# Copyright 2017 Vignesh @ Annadurai
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Twitter play",
    'summary': """ This App has the ability to Tweet as well as get auto Tweet from others, Have FUN  """,
    'version': '10.0.1.0.0',
    'category': 'tools',
    'website': "viki2.odoo.com",
    'author': "Vignesh",
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'images': ['images/main_screenshot.png'],
    'depends': ['base'],
    'data': [
         'data/twitter_cron.xml',
         'views/twitter_tweets.xml',
         'views/twitter_config.xml',
    ],
}