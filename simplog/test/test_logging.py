import pytest
import re

from datetime import datetime
from typing import Dict, Callable
from uuid import uuid4
from logger import (escape_backslash, escape_null, escape_newline, escape_quotes, escape_value, escape_tab,
                    force_string, quote_string, make_logger, refine_logger )


class TestEscapes(object):
    def test_escape_backslash_hasit_one(self):
        assert '\\\\' == escape_backslash('\\')

    def test_escape_backslash_hasit_two(self):
        assert 'One \\\\ Two \\\\ Three' == escape_backslash('One \\ Two \\ Three')

    def test_escape_backslash_nohas(self):
        assert 'One / Two / Three' == escape_backslash('One / Two / Three')

    def test_escape_backslash_empty(self):
        assert '' == escape_backslash('')


    def test_escape_tab_hasit_one(self):
        assert '\\t' == escape_tab('\t')

    def test_escape_tab_hasit_two(self):
        assert 'One \\t Two \\t Three' == escape_tab('One \t Two \t Three')

    def test_escape_tab_nohas(self):
        assert 'One / Two / Three' == escape_tab('One / Two / Three')

    def test_escape_tab_empty(self):
        assert '' == escape_tab('')


    def test_escape_newline_hasit_one(self):
        assert '\\n' == escape_newline('\n')

    def test_escape_newline_hasit_two(self):
        assert 'One \\n Two \\n Three' == escape_newline('One \n Two \n Three')

    def test_escape_newline_nohas(self):
        assert 'One / Two / Three' == escape_newline('One / Two / Three')

    def test_escape_newline_empty(self):
        assert '' == escape_newline('')


    def test_escape_null_hasit_one(self):
        assert '\\0' == escape_null('\0')

    def test_escape_null_hasit_two(self):
        assert 'One \\0 Two \\0 Three' == escape_null('One \0 Two \0 Three')

    def test_escape_null_nohas(self):
        assert 'One / Two / Three' == escape_null('One / Two / Three')

    def test_escape_null_empty(self):
        assert '' == escape_null('')


    def test_escape_quotes_one(self):
        assert "one 'two' three" == escape_quotes('one "two" three')

    def test_escape_quotes_two(self):
        assert 'He is 5\'10\\"' == escape_quotes('He is 5\'10"')

    def test_escape_quotes_nohas(self):
        assert 'One / Two / Three' == escape_quotes('One / Two / Three')

    def test_escape_quotes_empty(self):
        assert '' == escape_quotes('')

    
    def test_escape_value_everything(self):
        assert "\"one \\\\ \\\"two' \\n three \\0\"" == escape_value("one \\ \"two' \n three \0")

    def test_escape_value_nothing_with_quotes(self):
        assert '"one two three"' == escape_value('one two three')

    def test_escape_value_nothing(self):
        assert 'OneTwoThree' == escape_value('OneTwoThree')


class TestForceString(object):
    def test_string(self):
        assert "one two three" == force_string('one two three')

    def test_int(self):
        assert "123" == force_string(123)

    def test_list(self):
        assert "[1, 2, 3]" == force_string([1, 2, 3])

    def test_dict(self):
        assert "{'one': 1, 'two': 2, 'three': 3}" == force_string({'one': 1, 'two': 2, 'three': 3})


class TestQuoteString(object):
    def test_no_spaces_no_force(self):
        assert 'OneTwoThree' == quote_string('OneTwoThree')

    def test_no_spaces_force(self):
        assert '"OneTwoThree"' == quote_string('OneTwoThree', True)

    def test_with_spaces_no_force(self):
        assert '"One Two Three"' == quote_string('One Two Three')

    def test_with_spaces_force(self):
        assert '"One Two Three"' == quote_string('One Two Three', True)


def build_log_recorder(capture):
    def print_fn(s):
        capture['__log'] = s
    return print_fn


isoformat_re = r'\d{4}(-\d\d){2}T(\d\d:){2}\d\d(\.\d{1,6})?'  # rough approximation


class TestMakeLogger(object):
    def test_basic_logger(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder)
        log("Hey!")
        matchregex = f'{isoformat_re} level=info msg=Hey!'

        assert re.match(matchregex, capture['__log']) is not None
    
    def test_new_labels(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder, message_label='message', level_label='lvl')
        log("Hey!")
        matchregex = f'{isoformat_re} lvl=info message=Hey!'

        assert re.match(matchregex, capture['__log']) is not None

    def test_time_label(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder, time_label='app_time')
        log("Hey!")
        matchregex = f'app_time={isoformat_re} level=info msg=Hey!'

        assert re.match(matchregex, capture['__log']) is not None

    def test_logger_with_different_level(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder)
        log("Hey!", level='warn')
        matchregex = f'{isoformat_re} level=warn msg=Hey!'

        assert re.match(matchregex, capture['__log']) is not None

    def test_logger_with_extras(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder)
        log("Hey!", laser='beam')
        matchregex = f'{isoformat_re} level=info laser=beam msg=Hey!'

        assert re.match(matchregex, capture['__log']) is not None

    def test_logger_force_quotes(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder, force_quote=True)
        log("Hey!", meals='breakfast lunch dinner')
        matchregex = f'{isoformat_re} level="info" meals="breakfast lunch dinner" msg="Hey!"'
        
        assert re.match(matchregex, capture['__log']) is not None

    def test_logger_with_extras_with_spaces(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder)
        log("Hey!", panic='Maybe or maybe not')
        matchregex = f'{isoformat_re} level=info panic="Maybe or maybe not" msg=Hey!'

        assert re.match(matchregex, capture['__log']) is not None

    def test_refine_logger_one(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder)
        id = uuid4()
        clog = refine_logger(log, context=id)
        clog("Hey!")
        matchregex = f'{isoformat_re} level=info context={id} msg=Hey!'

        assert re.match(matchregex, capture['__log']) is not None

    def test_refine_logger_two(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder)
        id = uuid4()
        clog = refine_logger(log, context=id, color='red')
        clog("Hey!")
        this_or_that = f'((context={id} color=red)|(color=red context={id}))'
        matchregex = f'{isoformat_re} level=info {this_or_that} msg=Hey!'

        assert re.match(matchregex, capture['__log']) is not None

    def test_refine_logger_with_extras(self):
        capture = {}
        recorder = build_log_recorder(capture)
        log = make_logger(recorder)
        id = uuid4()
        clog = refine_logger(log, context=id)
        clog("Hey!", laser='beam')
        this_or_that = f'((context={id} laser=beam)|(laser=beam context={id}))'
        matchregex = f'{isoformat_re} level=info {this_or_that} msg=Hey!'

        assert re.match(matchregex, capture['__log']) is not None