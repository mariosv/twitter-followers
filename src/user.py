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

import twitter

from limiter import Rate_limited

class User(Rate_limited):
    """Wrapper around python-twitter User type, that is friendly to the
       twitter request rate limiting policy.

       Note that a connection(aka an instance of twitter.Api) reference is
       stored. It is needed in order to be able to call GetFollowers. followers
       is considered a reasonable attribute of a User.

    """
    def __init__(self, name_or_id, connection, limiter, twitter_api_user=None):
        super(User, self).__init__(limiter)
        self.__connection = connection
        self.__user = twitter_api_user
        self.__name_or_id = name_or_id
        if self.__user is None:
            self.__user = self.__create_user()

    @property
    @Rate_limited._decor
    def followers_count(self):
        return self.__user.GetFollowersCount()

    @property
    @Rate_limited._decor
    def protected(self):
        return self.__user.GetProtected()

    @property
    @Rate_limited._decor
    def screen_name(self):
        return self.__user.GetScreenName()

    @property
    @Rate_limited._decor
    def uid(self):
        return self.__user.GetId()

    @property
    @Rate_limited._decor
    def followers(self):
        t = self.__connection.GetFollowers(self.__name_or_id)
        return [User(x.screen_name, self.__connection, self.limiter, x) \
                for x in t]

    @property
    @Rate_limited._decor
    def follower_ids(self):
        return self.__connection.GetFollowerIDs(self.__name_or_id)['ids']

    @Rate_limited._decor
    def __create_user(self):
        return self.__connection.GetUser(self.__name_or_id)

    def __str__(self):
        return 'User(' + self.__name_or_id + ')'


