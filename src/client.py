# This file is part of twitter-followers.
#
# Copyright (C) 2013 Marios Visvardis <visvardis.marios@gmail.com>
#
# twitter-followers is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# twitter-followers is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with twitter-followers.  If not, see <http://www.gnu.org/licenses/>.

import sys

import twitter

from limiter import Limiter, Rate_limited
from user import User


class Client_error(Exception):
    def __init__(self, msg):
        super(Client_error, self).__init__(msg)


class Client(Rate_limited):
    """Twitter client that creates a connection on initialization.
       OAuth credentials must be provided via the conf option.
    
    """
    def __init__(self, conf):
        self.conf = conf
        self.__connect()
        limiter = Limiter(self.__con)
        super(Client, self).__init__(limiter)

    def get_user(self, name_or_id):
        return User(name_or_id, self.__con, self.limiter)

    def __connect(self):
        try:
            self.__con = twitter.Api(
                consumer_key=self.conf.consumer_key,
                consumer_secret=self.conf.consumer_secret,
                access_token_key=self.conf.request_token_url,
                access_token_secret=self.conf.access_token_url
            )
        except twitter.TwitterError as e:
            raise Client_error(str(e))

    @Rate_limited._decor
    def get_follower_ids(self, name_or_id):
        return self.__con.GetFollowerIDs(name_or_id)['ids']

