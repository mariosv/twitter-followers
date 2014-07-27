=================
twitter-network
=================

.. caution::
    This utility is no longer functional due to changes in the Twitter API


Overview
========

twitter-network is an utility that generates the graph of the network
of(around) a twitter user.

Should work with 2.6, 2.7, 3.3 and 3.4 Python versions


Usage
=====

The best way to define the required user credentials is to use a configuration
file.

An example file is supplied named cfg_example. Edit this file with the
appropriate values supplied by twitter.

Then run::

    python create_net.py -c cfg <user_name_or_id> <output_file> -d 2

where -d 2 defines the desired recursion depth.

