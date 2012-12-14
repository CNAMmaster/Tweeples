# Miscellaneous utility functions for Tweeple code
#
# This file is part of the Tweeples collection of scripts.
#
# Tweeples is free software: you can redistribute it and/or modify it
# under the terms of the BSD license. For the full terms of the license
# see the file `COPYING' in this directory.

import datetime
import sys

def warning(msgformat, *args):
    """Print a warning message to the standard error stream.

    Print 'WARNING: ' followed by a Python-formatted version of all of our
    arguments, to the standard error stream.

    Args:
        msgformat       str, A format-string to use for the rest of the
                        arguments of this function.
        args            list, A list of arguments whose types should be
                        printable according to the format specifiers of
                        'msgformat', e.g. if msgformat is '%d %d' there
                        should be two extra args that can be printed as
                        integer values.

    Returns:
        None
    """
    try:
        msg = msgformat % (args)
        print >> sys.stderr, 'WARNING:', msg
    except TypeError, e:
        print >> sys.stderr, 'Some args cannot be formatted for printing.'

def error(code, msgformat, *args):
    """Print an error message to the standard error stream and die.

    Print 'ERROR: ' followed by a Python-formatted version of all of our
    arguments, to the standard error stream, and then kill the current
    script with sys.exit.

    Args:
        code            int, An error code to pass to sys.exit.
        msgformat       str, A format-string to use for the rest of the
                        arguments of this function.
        args            list, A list of arguments whose types should be
                        printable according to the format specifiers of
                        'msgformat', e.g. if msgformat is '%d %d' there
                        should be two extra args that can be printed as
                        integer values.

    Returns:
        None
    """
    try:
        code = int(code)
        msg = msgformat % (args)
        print >> sys.stderr, 'ERROR:', msg
    except ValueError, e:               # code is not an 'int' value
        sys.exit(1)
    except TypeError, e:
        print >> sys.stderr, 'Some args cannot be formatted for printing.'
        sys.exit(1)
    sys.exit(code)

def message(msgformat, *args):
    """Print a time-stamped formatted message to the standard error stream.

    Print the current time, followed by a formatted message of all of our
    arguments, to the standard error stream.

    Args:
        msgformat       str, A format-string to use for the rest of the
                        arguments of this function.
        args            list, A list of arguments whose types should be
                        printable according to the format specifiers of
                        'msgformat', e.g. if msgformat is '%d %d' there
                        should be two extra args that can be printed as
                        integer values.

    Returns:
        None
    """
    try:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = msgformat % (args)
        print >> sys.stderr, timestamp, msg
    except TypeError, e:
        print >> sys.stderr, 'Some args cannot be formatted for printing.'
        sys.exit(1)
