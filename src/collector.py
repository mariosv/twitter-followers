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

import networkx as nx

import twitter

class Collector(object):
    """When collect() is called follower nodes are recursively visited and
       their connections are saved in a graph structure.

       Usage:

           Collector must be initialized with a connected Client instance.
           Call collect() to start the process and collect the results via the
           graph attribute.

    """

    def __init__(self, client):
        self.__client = client
        self.graph = nx.DiGraph()
        self.__visited = []

    def collect(self, start):
        self.__visit(start.uid, self.__client.conf.depth)

    def __visit(self, uid, depth):
        # terminate recursion
        if(depth) == 0:
            return
        depth -= 1
        f = []
        try:
            f = self.__client.get_follower_ids(uid)
        except twitter.TwitterError:
            # in case we are not authorized to get the follower ids for an
            # account, the account is probably protected. do nothing
            pass
        print('%d followers: %d' % (uid, len(f)))
        for i in f:
            self.graph.add_edge(i, uid)
            if i in self.__visited:
                continue
            self.__visit(i, depth)
        self.__visited.append(uid)

