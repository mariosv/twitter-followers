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
import networkx as nx

from client import Client_error

class Collector(object):
    """When collect() is called follower nodes are recursively visited and
       their connections are saved in a graph structure.

       Usage:

           Collector must be initialized with a connected Client instance.
           Call collect() to start the process and collect the results via the
           graph attribute.

    """

    def __init__(self, client, conf):
        self._client = client
        self._conf = conf
        self._visited = set()
        self.graph = nx.DiGraph()

    def collect(self, start_node):
        self._visit(start_node, self._conf.depth)

    def _visit(self, uid, depth):
        # terminate recursion
        if(depth) == 0:
            return
        depth -= 1
        f = None
        try:
            try:
                cuid = int(uid)
                ctype = 'user_id'
            except:
                cuid = uid
                ctype = 'screen_name'
            f = self._client.get_followers(**{ctype: cuid})
        except Client_error as e:
            sys.stderr.write('Error: %s\n' % str(e))
            sys.exit(1)
        print('%s followers: %d' % (str(uid), len(f)))
        for i in f:
            self.graph.add_edge(i, uid)
            if i in self._visited:
                continue
            self._visit(i, depth)
        self._visited.add(uid)

