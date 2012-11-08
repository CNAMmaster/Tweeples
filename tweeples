#!/usr/bin/env python
#
# Tweeples - Mine Twitter for people relationships

import datetime
import errno
import getopt
import json
import os
import sys
import twitter

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

def streamsearch(ofile, text, max_pages=10, results_per_page=100):
    """Stream the results of searching for 'text' to the 'ofile' output file

    Args:
      ofile             str, the name of a file where we will write any tweets
                        we find. Tweets are written in JSON format, with every
                        tweet being stored in a separate dict of key-value
                        pairs like 'id', 'text', etc. The dict is one of the
                        results from twitter.Twitter.search().
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
    seen = {}
    try:
        tweetfile = file(json_filename, 'r')
        seen = dict((tweet['id'], True)
                    for tweet in [json.loads(line)
                                  for line in tweetfile.readlines()])
        tweetfile.close()
    except IOError, e:
        if e.errno == errno.ENOENT:
            pass
        else:
            error(1, 'Cannot pre-load seen tweets: %s', e)
            return None
    if seen:
        message('%d tweets preloaded from %s', len(sorted(seen)), ofile)
    try:
        ostream = file(ofile, 'a+')
        for matches in search(text, max_pages=max_pages,
                              results_per_page=results_per_page):
            newmatches = 0
            for tweet in matches:
                (tid, tuser, text) = (tweet['id'], tweet['from_user'],
                                      tweet['text'])
                if not tid in seen:
                    newmatches += 1
                    seen[tid] = True
                    print >> ostream, json.dumps(tweet)
            if newmatches > 0:
                message('%d new tweets logged at %s', newmatches, ofile)
    except IOError, e:
        warning('Error writing at file "%s". %s', ofile, e)
        return None

if __name__ == '__main__':
    json_filename = 'tweets.json'       # default output file name
    lookup_text = '#7ngr'               # default search string

    # Parse command-line args for output file name.
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'o:')
    except getopt.GetoptError, e:
        error(1, '%s', e)

    for opt, value in optlist:
        if opt == '-o' and value:
            json_filename = value       # custom output file
            message('Output file: %s', json_filename)
    if len(args) > 0:
        # custom lookup text
        lookup_text = ' '.join(args)
        message('Lookup text: %s', lookup_text)

    while True:
        try:
            streamsearch(json_filename, lookup_text)
        except TwitterHTTPError, e:
            warning('Skipping HTTP error %s [...]', str(e).split('\n')[0])
            pass
