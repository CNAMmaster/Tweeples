# Tweeples.util - miscellaneous utility functions for Tweeple code
#
# Copyright (C) 2012, Giorgos Keramidas <gkeramidas@google.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

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
