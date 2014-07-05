=================
twitter-followers
=================

.. caution::
    This utility is no longer functional due to changes in the Twitter API


Overview
========

twitter-followers is an utility that generates the graph of the followers
of a twitter user.

The twitter request rate limiting policy is respected.

A twitter user account is required and the appropriate credentials in order
to be able to use the Twitter API via oauth.

The graph is exported as a Graphviz dot file.

python-twitter and networkx libraries are used.



Usage
=====

The best way to define the required user credentials is to use a configuration
file.

An example file is supplied named cfg_example. Edit this file with the
appropriate values supplied by twitter.

Then run::

    python twitter_graph_gen.py -c cfg <user_name_or_id> <output_file> -d 2

where -d 2 defines the desired recursion depth.

