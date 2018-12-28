"""Logging and Profiling
"""

import time as time_module
import datetime
import logging

from colorama import Fore, Style

from webflowpy import settings

_previous_memory_usage = -1

logger = logging.getLogger('webflowpy')
logger.propagate = False  # Don’t pass log messages on to logging.root and its handler
logger.setLevel('INFO')
logger.addHandler(logging.StreamHandler())  # Logs go to stderr
logger.handlers[-1].setFormatter(logging.Formatter('%(message)s'))
logger.handlers[-1].setLevel('INFO')

def get_logger(name):
    """Creates a child logger that delegates to pypairs_logger instead to logging.root"""
    return logger.manager.getLogger(name)


_VERBOSITY_LEVELS_FROM_STRINGS = {
    'error': 0,
    'warn': 1,
    'status': 2,
    'info': 3
}

def get_time_formatted():
    return time_module.strftime("%H:%M:%S", time_module.gmtime())


def status(*args, **kwargs):
    str = "{} [{}{}{}]".format(get_time_formatted(), Fore.GREEN, 'STAT', Style.RESET_ALL)
    args = (str, ) + args
    return msg(*args, v='status', **kwargs)


def error(*args, **kwargs):
    str = "{} [{}{}{}]".format(get_time_formatted(), Fore.RED, 'ERR ', Style.RESET_ALL)
    args = (str,) + args
    return msg(*args, v='error', **kwargs)


def warn(*args, **kwargs):
    str = "{} [{}{}{}]".format(get_time_formatted(), Fore.YELLOW, 'WARN', Style.RESET_ALL)
    args = (str,) + args
    return msg(*args, v='warn', **kwargs)


def info(*args, **kwargs):
    str = "{} [{}{}{}]".format(get_time_formatted(), Fore.BLUE, 'INFO', Style.RESET_ALL)
    args = (str,) + args
    return msg(*args, v='info', **kwargs)


def _settings_verbosity_greater_or_equal_than(v):
    if isinstance(settings.verbosity, str):
        settings_v = _VERBOSITY_LEVELS_FROM_STRINGS[settings.verbosity]
    else:
        settings_v = settings.verbosity
    return settings_v >= v


def msg(*msg, v=4, time=False, reset=False, end='\n',
        no_indent=False, t=None, r=None):
    """Write message to logging output.
    Log output defaults to standard output but can be set to a file
    by setting `sc.settings.log_file = 'mylogfile.txt'`.
    v : {'error', 'warn', 'status', 'info'} or int, (default: 4)
        0/'error', 1/'warn', 2/'status', 3/'info', 4, 5, 6...
    time, t : bool, optional (default: False)
        Print timing information; restart the clock.
    memory, m : bool, optional (default: Faulse)
        Print memory information.
    reset, r : bool, optional (default: False)
        Reset timing and memory measurement. Is automatically reset
        when passing one of ``time`` or ``memory``.
    end : str (default: '\n')
        Same meaning as in builtin ``print()`` function.
    no_indent : bool (default: False)
        Do not indent for ``v >= 4``.
    """
    # variable shortcuts
    if t is not None: time = t
    if r is not None: reset = r
    if isinstance(v, str):
        v = _VERBOSITY_LEVELS_FROM_STRINGS[v]
    #if v == 3:  # insert "--> " before infos
    #    msg = ('-->',) + msg
    #if v >= 4 and not no_indent:
    #    msg = ('   ',) + msg
    if _settings_verbosity_greater_or_equal_than(v):
        if not time and len(msg) > 0:
            _write_log(*msg, end=end)
        if reset:
            settings._previous_time = time_module.time()
        if time:
            elapsed = get_passed_time()
            msg = msg + ('({})'.format(_sec_to_str(elapsed)),)
            _write_log(*msg, end=end)

m = msg  # backwards compat

def _write_log(*msg, end='\n'):
    """Write message to log output, ignoring the verbosity level.
    This is the most basic function.
    Parameters
    ----------
    *msg :
        One or more arguments to be formatted as string. Same behavior as print
        function.
    """
    from webflowpy.settings import logfile
    if logfile == '':
        print(*msg, end=end)
    else:
        out = ''
        for s in msg:
            out += str(s) + ' '
        with open(logfile, 'a') as f:
            f.write(out + end)


def _sec_to_str(t):
    """Format time in seconds.
    Parameters
    ----------
    t : int
        Time in seconds.
    """
    from functools import reduce
    return "%d:%02d:%02d.%02d" % \
        reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
               [(t*100,), 100, 60, 60])


def get_passed_time():
    now = time_module.time()
    elapsed = now - settings._previous_time
    settings._previous_time = now
    return elapsed

def get_date_string():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")