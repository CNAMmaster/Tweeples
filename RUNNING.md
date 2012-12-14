============================
Running the Tweeples Scripts
============================

The scripts contained in this directory should be self-contained Python
code.  External dependencies are imported in their own package directory
and are usable directly from this source tree, without having to
separately install extra Python packages.

The source code of the scripts is separated in two parts:

  - Driving scripts, that can be run independently and depend on other
    parts of this source tree.
  - Dependencies of the driver scripts.  These are Python packages that
    are imported from the rest of the code.

The convention used when adding new scripts to this directory is that
driver scripts are called *tool_xxx.py* and the rest of the code follows
a simple rule for directory layout / organization: "anything that is
commonly shared by driver scripts is in a reasonably flat collection of
*xxx.py* files if I have written it, or in a subdirectory if it has been
imported from elsewhere".

================
Toplevel Scripts
================

There are currently the following top-level scripts in this source tree:

- `tool_collect_tweets.py`
  A script that can collect tweets matching a hash tag or a plain
  string, and store them in json-compatible lines in a simple text file.

==============================================
Collecting Tweets Matching a String or Hashtag
==============================================

The `tool_collect_tweets.py` script can collect tweets matching a string
or hash tag.  It may be run with a simple string to search for, and it
will query the public Twitter timeline for tweets matching this string.

For example, the following invocation will look for tweets matching the
text "freebsd" and print a single json-formatted line for each matching
tweet:

    ./tool_collect_tweets.py freebsd

The tweets will be printed to standard output, but may be redirected to
a text file by the *-o* option:

    ./tool_collect_tweets.py -o freebsd.json freebsd

The script will keep running and querying the public Twitter timeline
forever, so to interrupt it just kill it with *Ctrl-C* or by any other
signal that normally terminates a program (`SIGTERM` should also work
fine, for instance).
