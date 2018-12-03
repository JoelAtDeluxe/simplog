from functools import partial
from datetime import datetime
from typing import Callable, Any


def force_string(s: Any) -> str:
    return f'{s}'


def escape_value(s: Any, to_str_func: Callable[[Any], str]=force_string, force_quotes=False) -> str: 
    stringified = to_str_func(s)
    escape_funcs = [
        escape_backslash,
        escape_null,
        escape_newline,
        escape_tab,
        escape_quotes,
        lambda x: quote_string(x, force_quotes),  # Maybe this should be done via partial... maybe passed in to pre-compile it then?
    ]

    for step in escape_funcs:
        stringified = step(stringified)

    return stringified


def escape_backslash(s: str) -> str: 
    return s.replace('\\', '\\\\')


def escape_newline(s: str) -> str:
    return s.replace('\n', '\\n')  # Todo: replace with re.sub and factor in \r

def escape_tab(s: str) -> str:
    return s.replace('\t', '\\t')

def escape_null(s: str) -> str:
    return s.replace("\0", "\\0")


def escape_quotes(s: str) -> str:
    if "'" in s:
        return s.replace('"', '\\"')
    return s.replace('"', "'")


def quote_string(s: str, force=False) -> str:
    return f'"{s}"' if force or ' ' in s else s


def make_logger(write_func=print, *, message_label="msg", level_label="level", time_label=None, 
                to_string_func=force_string, force_quote=False):
    time_label = '' if time_label is None else f'{time_label}='
    esc = lambda m: escape_value(m, to_string_func, force_quote)

    def log(message, level='info', **kwargs) -> None:
        now = f'{time_label}{datetime.now().isoformat()}'
        msg = f'{message_label}={esc(message)}'
        lvl = f'{level_label}={esc(level)}'

        v_fields = [] if kwargs == {} else (f'{k}={esc(v)}' for k, v in kwargs.items())

        line = f'{now} {lvl} {" ".join(v_fields)}{" " if v_fields else ""}{msg}'
        write_func(line)

    return log


def refine_logger(logger, **kwargs):
    return partial(logger, **kwargs)
