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

import time

import twitter

class Limiter(object):
    """Checks the remaining allowed requests to the twitter API and keeps
       track of the requests done in order to not exceed the limit.

       Should be initialize with a valid connection(twitter.API) object.

       Method check_and_wait should be used before a Rate limited operation
       is called in order to make sure the rate limiting policy is not violated.
       check_and_wait checks if the limit is exceeded and if it does
       waits until the limit is reset.

    """
    def __init__(self, connection):
        self._connection = connection
        self._limit = self._check_status()[0]

    def check_and_wait(self):
        self._limit -= 1
        if self._limit <= 0:
            print('Rate limit hit!')
            self._limit, time_delta = self._check_status()
            while self._limit == 0:
                print('Waiting for %d seconds' % time_delta)
                time.sleep(time_delta)
                self._limit, time_delta = self._check_status()
            print("New limit: " + str(self._limit))

    def _check_status(self):
        r = self._connection.GetRateLimitStatus()
        remaining = r['remaining_hits']
        next_reset_delta = int(r['reset_time_in_seconds'] - time.time())
        return remaining, next_reset_delta

    def __str__(self):
        return str(self.val)


class Rate_limited(object):
    """Convinience base class for types that require rate limited operations.
       Descendant types should initialize it with a (typically shared)Limiter
       instance.

       The supplied static method should be used to decorate rate limited
       operations.
    
    """

    def __init__(self, limiter):
        self.limiter = limiter

    @staticmethod
    def _decor(fun):
        """Twitter API request counting decorator. staticmethod to trick in
           order to make decorators work properly with inheritance

        """
        def counted(self, *args):
            self.limiter.check_and_wait()
            return fun(self, *args)
        return counted


