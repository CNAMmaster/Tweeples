#!/usr/bin/env python

'''Collect tweets matching a text pattern and store them
continuously in JSON-formatted lines of a local file.'''

__author__ = 'Giorgos Keramidas <gkeramidas@gmail.com>'

import argparse
import errno
import json
import os
import sys
import twitter

from twitter.api import TwitterHTTPError

from util import error, message, warning

def search(text, max_pages=10, results_per_page=100):
    """Generator for searching 'text' in Twitter content

    Search the public Twitter timeline for tweets matching a 'text' string,
    which can also be a hash tag, and yield a batch of matched tweets every
    time we have some results.

    Args:
      text              str, the text to search for in Twitter. This can
                        be a plain text string or a '#hashtag' to look
                        for tweets of this topic only.
      max_pages         int, maximum number of result 'pages' to obtain
                        from Twitter's backlog of archived tweets. When
                        not specified, default to 10 pages.
      results_per_page  int, maximum number of results per page to fetch
                        from Twitter's backlog of archived tweets. When
                        not specified, default to 100 tweets per page.

    Returns:
      An array of dicts. Every dict in the returned array is a 'result' from
      twitter.Twitter.search and represents a single tweet.
    """
    while True:
        t = twitter.Twitter(domain="search.twitter.com")
        for page in range(1, max_pages + 1):
            yield t.search(q=text, rpp=results_per_page, page=page)['results']

def preload_tweets(filename):
    """Preload previously seen tweets from a text file.

    Args:
        filename        str, Name of the file where we preload tweets from.

    Returns:
        A set() containing all the numeric 'id' attributes of tweets we have
        already seen.
    """
    if not filename:
        return set()
    seen = set()
    try:
        stream = file(json_filename, 'r')
        for id in (tweet['id'] for tweet in
                      (json.loads(line) for line in stream.readlines())):
            seen.add(id)
        stream.close()
    except Exception, e:
        seen = set()            # Avoid returning partial results on error
    return seen

def streamsearch(ofile, text, max_pages=10, results_per_page=100):
    """Stream the results of searching for 'text' to the 'ofile' output file

    Args:
      ofile             str, the name of a file where we will write any tweets
                        we find. Tweets are written in JSON format, with every
                        tweet being stored in a separate line as a Python dict.
      text              str, the text to search for in Twitter. This can
                        be a plain text string or a '#hashtag' to look
                        for tweets of this topic only.
      max_pages         int, maximum number of result 'pages' to obtain
                        from Twitter's backlog of archived tweets. When
                        not specified, default to 10 pages.
      results_per_page  int, maximum number of results per page to fetch
                        from Twitter's backlog of archived tweets. When
                        not specified, default to 100 tweets per page.

    Returns:
      None
    """
    # Load the id of already seen tweets, if there are any.
    seen = ofile and preload_tweets(ofile) or set()
    if seen:
        message('%d tweets preloaded from %s', len(seen), ofile)
    try:
        ostream = ofile and file(ofile, 'a+') or sys.stdout
        for matches in search(text, max_pages=max_pages,
                              results_per_page=results_per_page):
            newmatches = 0
            for tweet in matches:
                (tid, tuser, text) = (tweet['id'], tweet['from_user'],
                                      tweet['text'])
                if not tid in seen:
                    newmatches += 1
                    seen.add(tid)
                    print >> ostream, json.dumps(tweet)
            if newmatches > 0:
                message('%d new tweets logged at %s', newmatches,
                    ofile or 'standard output')
    except IOError, e:
        warning('Error writing at file "%s". %s', ofile, e)
        return None

if __name__ == '__main__':
    json_filename = None                # Where to store matching tweets
    lookup_text = None                  # Text to search for

    # Parse command-line args for output file name.
    parser = argparse.ArgumentParser(description=(
        'Collect tweets matching a text pattern and store them'
        'continuously in JSON-formatted lines of a local file.'))
    parser.add_argument('-o', '--output', metavar='FILE', type=str,
        default=None, help='output file name')
    parser.add_argument('TEXT', nargs='+', type=str, default=None,
        help='text to search for in tweet content')
    args = parser.parse_args()

    json_filename = args.output         # Where to store matching tweets
    lookup_text = ' '.join(args.TEXT)   # Text to search for

    # Keep searching for tweets, until manually interrupted.
    while True:
        try:
            streamsearch(json_filename, lookup_text)
        except TwitterHTTPError, e:
            warning('Skipping HTTP error %s [...]', str(e).split('\n')[0])
            pass
