# -*- coding: utf-8 -*-
# Copyright 2017 Vignesh @ Annadurai
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# pip install tweepy
# http://tweepy.readthedocs.io/en/v3.5.0/api.html#timeline-methods
#pip install tweepy==3.3.0
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import uuid

import tweepy
from tweepy import OAuthHandler,TweepError
from tweepy.streaming import StreamListener
import time
from tweepy import Stream
import random


class twitterCase(models.Model):
    _name = 'twitter.config'
    _rec_name = "account_name"
    
    account_name = fields.Char(string="Name/ID", required = True, help="For identify account")
    consumer_key = fields.Char(string="Consumer key", required = True, help="Provide Twitter Consumer Key")
    consumer_secret = fields.Char(string="Consumer Secret", required = True, help="Provide Twitter Consumer SecretKey")
    access_token = fields.Char(string="Access Token", required = True, help="Provide Twitter Access Token")
    access_secret = fields.Char(string="Access Secret", required = True, help="Provide Twitter Access secret key")

class twitterTweet(models.Model):
    _name = 'twitter.test'
    _inherit = 'twitter.config'

    twitter_account = fields.Many2one('twitter.config',string= "Twitter Account", required = True, help="Provide Twitter Account")
    user_name = fields.Char(string="User Name/ user ID", required = True)
    tw_hashtag = fields.Char(string="HashTag")
    twitter_home_feed = fields.Text(string="Home feeds")
    twitter_timeline_feed = fields.Text(string="User feeds")
    twitter_all = fields.Html(string="Home User feeds")
    twitter_status_update = fields.Char(string="Update Status",size=139)
    twitter_followers_count = fields.Char("Followers_count")
    twitter_uuid = fields.Char('UUID', default=lambda s: uuid.uuid4(), copy=False, required=True, readonly= True)
    twitter_other_user = fields.Char(string="Check other user Tweets")
    twitter_other_user_tweets = fields.Char(string="Other user Tweets")
    twitter_other_user_screen_name = fields.Char(string="Other user ScreenName")
    twitter_other_user_follower_count = fields.Char(string="Other user FollowersCount")
    twitter_other_user_friend_list = fields.Char(string="Check other user friendList")
    twitter_other_user_follower_ids = fields.Char(string="other user FollowersID's")
    twitter_stream_filter = fields.Char(string="Stream_filter")
    twitter_status_location = fields.Char( string="Location")

    @api.multi
    @api.model
    def checkOtherstweet(self):
        auth = OAuthHandler(self.twitter_account.consumer_key, self.twitter_account.consumer_secret)
        auth.set_access_token(self.twitter_account.access_token, self.twitter_account.access_secret)
        t_api = tweepy.API(auth)

        self.ensure_one()
        user = t_api.get_user(self.twitter_other_user)
        if not self.twitter_other_user:
            raise ValidationError(_('InvalidUser ID'))
        else:
            try:
                self.twitter_other_user_tweets = user.status.text
            except ValueError:
                raise ValidationError(_('not having status'))
            self.twitter_other_user_screen_name = user.screen_name
            self.twitter_other_user_follower_count = user.followers_count
            self.twitter_status_location = user.location
            friends= []
            for friend in user.friends():
                friends.append(str(friend.screen_name))
                self.twitter_other_user_friend_list = str(friends)

    @api.multi
    @api.model
    def checktweet(self):
        auth = OAuthHandler(self.twitter_account.consumer_key, self.twitter_account.consumer_secret)
        auth.set_access_token(self.twitter_account.access_token, self.twitter_account.access_secret)
        t_api = tweepy.API(auth)

        self.ensure_one()
        for status in tweepy.Cursor(t_api.home_timeline).items(10):
            if status.text:
                self.twitter_home_feed = status.text

        user = t_api.get_user(self.user_name)
        for friend in user.friends():
            self.twitter_followers_count = friend.screen_name

        for status in tweepy.Cursor(t_api.user_timeline).items(10):
            if status.text:
                self.twitter_timeline_feed = status.text
#
        twitterStream = tweepy.streaming.Stream(auth, tweepy.StreamListener()) #initialize Stream object with a time out limit
        if self.tw_hashtag:
            tw_stream = twitterStream.filter(track=["#"+self.tw_hashtag], async = True) #, languages=['en'].
            self.twitter_stream_filter = tw_stream

#for CRON job play. Post tweets for every single minute with hashable value

    @api.one
    @api.model
    def updatetweet(self):
        auth = OAuthHandler(self.twitter_account.consumer_key, self.twitter_account.consumer_secret)
        auth.set_access_token(self.twitter_account.access_token, self.twitter_account.access_secret)
        t_api = tweepy.API(auth)

        self.ensure_one()
#        sliced = self.twitter_uuid[:4]
        sliced = str(random.random())[:4]
#        for status in tweepy.Cursor(t_api.user_timeline).items(10):i
        status_update = str(self.twitter_status_update +" "+ sliced)
        try:
            tweepy.Cursor(t_api.update_status(status=status_update))
        except TweepError as e:
            raise ValidationError(_('Status updated successfully! Just ignore this {} error \n'.format(e)))
        self.twitter_status_update = tweepy.Cursor(t_api.update_status(status=status_update))
        return

