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
import os
import time

import argparse
import ConfigParser

import networkx as nx

from client import Client
from collector import Collector


def parse_options():
    """Parses the configuration file and the command line options. Command
       line options override values found in the configuration file.
       The trick described in http://stackoverflow.com/a/5826167 is used

    """
    cfg_parser = argparse.ArgumentParser(add_help=False)

    cfg_parser.add_argument("-c", "--config", help="Configuration file",
                            metavar="FILE")
    args, remaining_argv = cfg_parser.parse_known_args()
    defaults = {}
    if args.config:
        cfg = ConfigParser.SafeConfigParser()
        cfg.read([args.config])
        defaults = dict(cfg.items("Auth"))

    # parse the rest of the arguments (command line))
    parser = argparse.ArgumentParser(parents=[cfg_parser])
    parser.set_defaults(**defaults)

    parser.add_argument("--consumer_key", help="twitter API key")
    parser.add_argument("--consumer_secret", help="twitter API secret")
    parser.add_argument("--request_token_url",
                        help="twitter API request token url")
    parser.add_argument("--auth_url", help="twitter API auth url")
    parser.add_argument("--access_token_url",
                        help="twitter API access token url")

    parser.add_argument("-d", "--depth", default=1, type=int,
                        help="search recursion depth")
    # starting user name or id is a positional argument
    parser.add_argument("start_user",
        help="The Twitter user(screen_name or id) to start from.")

    parser.add_argument("output_file",
        help="The desired name for the Graphviz dot output file")
       
    args = parser.parse_args(remaining_argv)
    return args
         

def main():
    conf = parse_options()

    c = Client(conf)
    collector = Collector(c)
    start = c.get_user(conf.start_user)
    collector.collect(start)

    g = collector.graph
    nx.write_dot(g, conf.output_file)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

