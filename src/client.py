# This file is part of twitter-network.
#
# Copyright (C) 2013-2014 Marios Visvardis <visvardis.marios@gmail.com>
#
# twitter-network is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# twitter-network is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with twitter-network.  If not, see <http://www.gnu.org/licenses/>.
"""Implementation of a Client for the Twitter REST API v.1.1.

   Parts of the code are based on the twitter-application-only-auth project
   <https://github.com/pabluk/twitter-application-only-auth>.
   Especially parts related to Python versions compatibility.
   
"""
import sys
import base64
import json
import time

try:
    # For Python 3.0 and later
    import urllib
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
    from urllib.parse import quote, urlencode
except:
    from urllib2 import urlopen, Request, HTTPError, quote
    from urllib import urlencode


class Client_error(Exception):
    def __init__(self, msg):
        super(Client_error, self).__init__(msg)


class Client(object):
    """Client for the Twitter REST API v1.1. Only network discovery(followers,
       friends) operations are supported.
    
       The Twitter rate limiting policy is respected. If the rate limit
       is hit the program blocks until the next time window when the limit
       is reset

    """
    def __init__(self, conf):
        self._conf = conf
        self._access_token = self._get_access_token()

    def get_followers(self, **kwargs):
        """Returns a list of the ids of the followers of the requested user.
           Either user_id=id or screen_name=scr_name keyword arguments can be
           used to specify the user.

        """
        idtype, idval = self._get_id(kwargs)
        url = self._conf.request_followers_url
        params = urlencode({idtype: idval})
        url += '?' + params
        return self._collect_result_ids(url)

    def get_friends(self, user_id):
        idtype, idval = self._get_id(kwargs)
        url = self._conf.request_friends_url
        params = urlencode({idtype: idval})
        url += '?' + params
        return self._collect_result_ids(url)

    # -------------------------------------------------------------------------
    def _get_id(self, args):
        """Dispatches function calls with user_id and screen_name arguments"""
        idtype = 'user_id'
        idval = None
        if 'user_id' in args.keys():
            assert 'screen_name' not in args.keys()
            idval = args['user_id']
        else:
            assert 'screen_name' in args.keys()
            idtype = 'screen_name'
            idval = args['screen_name']
        return idtype, idval

    def _collect_result_ids(self, url):
        """This function handles multi-page results. See more about cursoring:
           https://dev.twitter.com/docs/misc/cursoring for more details

        """
        ids = []
        cursor = -1
        while True:
            cursored_url = url + '&cursor=' + str(cursor)
            response = self._auth_request(cursored_url)
            ids += response['ids']
            cursor = int(response['next_cursor'])
            print('Ids retrieved: %d' % len(ids))
            if 0 == cursor:
                break
        return ids

    def _auth_request(self, url):
        """Adds auth header and sends the given REST request"""
        request = Request(url)
        request.add_header('Authorization', 'Bearer %s' % self._access_token)
        try:
            response = urlopen(request)
        except HTTPError as e:
            raise Client_error('Error loading url %s: %s' % (url, str(e)))
        raw_data = response.read().decode('utf-8')
        self._check_rate_limiting_and_wait(response.info())
        data = json.loads(raw_data)
        return data

    def _check_rate_limiting_and_wait(self, response_header):
        """Read the HTTP response to find the number of requests of this
           type allowed for the current time window. If the rate limit was hit,
           wait(block) until the next window
        """
        rate_limit_remaining = int(response_header['X-Rate-Limit-Remaining'])
        print("%d requests remaining" % (rate_limit_remaining))
        if 0 == rate_limit_remaining:
            next_window_time = int(response_header['X-Rate-Limit-Reset'])
            # TODO: parse Date field to get the current "twitter" time
            print('Date', response_header['Date'])
            next_window_delta = next_window_time - time.time()
            # XXX: workaround.. sleeping 15 minutes
            next_window_delta = 900
            print('Request limit hit: sleeping for %d seconds' \
                  % (next_window_delta))
            time.sleep(next_window_delta)

    def _encode_key_and_secret(self, consumer_key, consumer_secret):
        ck = quote(consumer_key)
        cs = quote(consumer_secret)
        s = ck + ':' + cs
        encoded = base64.b64encode(s.encode('ascii'))
        return encoded

    def _get_access_token(self):
        encoded = self._encode_key_and_secret(self._conf.consumer_key,
                                              self._conf.consumer_secret)
        request = Request(self._conf.request_token_url)
        request.add_header('Content-Type',
                           'application/x-www-form-urlencoded;charset=UTF-8')
        request.add_header('Authorization',
                           'Basic %s' % encoded.decode('utf-8'))
        request_data = 'grant_type=client_credentials'.encode('ascii')
        if sys.version_info < (3,4):
            request.add_data(request_data)
        else:
            request.data = request_data

        try:
            response = urlopen(request)
        except HTTPError as e:
            raise Client_error(str(e) + str(e.read()))

        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data['access_token']
