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
    def __init__(self, conf):
        self._access_token = self._get_access_token(conf)

    def get_followers(self, user_id):
        pass

    def get_friends(self, user_id):
        pass

    # -------------------------------------------------------------------------
    def _auth_request(self, url):
        """Adds auth header and sends the given REST request"""
        request = Request(url)
        request.add_header('Authorization', 'Bearer %s' % self._access_token)
        try:
            response = urlopen(request)
        except HTTPError as e:
            raise Client_error(str(e))
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data

    def _encode_key_and_secret(self, consumer_key, consumer_secret):
        ck = quote(consumer_key)
        cs = quote(consumer_secret)
        s = ck + ':' + cs
        encoded = base64.b64encode(s.encode('ascii'))
        return encoded

    def _get_access_token(self, conf):
        encoded = self._encode_key_and_secret(conf.consumer_key,
                                              conf.consumer_secret)
        request = Request(conf.request_token_url)
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
