# This file is part of twitter-network.
#
# Copyright (C) 2013 Marios Visvardis <visvardis.marios@gmail.com>
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
import argparse
import networkx as nx

try:
    # Python >3
    from configparser import SafeConfigParser
except:
    from ConfigParser import SafeConfigParser

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
        cfg = SafeConfigParser()
        cfg.read([args.config])
        defaults = dict(cfg.items("Auth"))

    # parse the rest of the arguments (command line))
    parser = argparse.ArgumentParser(parents=[cfg_parser])
    parser.set_defaults(**defaults)

    endpoint = 'https://api.twitter.com/'

    parser.add_argument("--consumer_key", help="twitter API key")
    parser.add_argument("--consumer_secret", help="twitter API secret")
    parser.add_argument("--request_token_url",
                        default=endpoint + 'oauth2/token',
                        help="twitter API request token url")
    parser.add_argument('--request_rate_limit',
                        default=endpoint \
                                + '1.1/application/rate_limit_status.json',
                        help="twitter API rate limit request url")
    parser.add_argument('--request_friends_url',
                        default=endpoint + '1.1/friends/ids.json',
                        help="twitter API friends/ids request url")
    parser.add_argument('--request_followers_url',
                        default=endpoint + '1.1/followers/ids.json',
                        help="twitter API followers/ids request url")
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
    client = Client(conf)
    collector = Collector(client, conf)
    collector.collect(conf.start_user)
    nx.write_dot(collector.graph, conf.output_file)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
