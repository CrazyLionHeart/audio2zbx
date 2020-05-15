#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the MIT license.

from datetime import datetime, timedelta

from main import match_replace
from main import parse_EventLogGetLog
from main import parse_EventLogGetLogNumber
from main import parse_devstatus_error
from main import type_needle

import pytest

testdata_match_replace = [
    ("none", {
        "needle": type_needle,
        "result": ""
    }
    ),
    ("flt", {
        "needle":
        type_needle,
        "result": "FAULT"
    }
    ),
    ("err", {
        "needle": type_needle,
        "result": "ERROR"
    }
    ),
    ("wrn", {
        "needle": type_needle,
        "result": "WARNING"
    }
    ),
]

testdata_devstatus_error = [
    ('OK devstatus error "none"', {
        "type": "",
        "message": "",
        "alert_id": 0x10,
        "alert": "off",
        "alert_count": 0,
        "unit_id": 0x100,
        "date": datetime(1970, 1, 1, 0, 0, 0)
    }),
    ('OK devstatus error "flt/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"', {
        "type": "FAULT",
        "message": "DCP[0] communication error",
        "alert_id": 0x53,
        "alert": "on",
        "alert_count": 1,
        "unit_id": 0x001,
        "date": datetime.strptime("2013/1/22 11:38:23",
                                  '%Y/%m/%d %H:%M:%S')
    }),
    ('OK devstatus error "err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"', {
        "type": "ERROR",
        "message": "DCP[0] communication error",
        "alert_id": 0x53,
        "alert": "on",
        "alert_count": 1,
        "unit_id": 0x001,
        "date": datetime.strptime("2013/1/22 11:38:23",
                                  '%Y/%m/%d %H:%M:%S')
    }),
    ('OK devstatus error "wrn/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"', {
        "type": "WARNING",
        "message": "DCP[0] communication error",
        "alert_id": 0x53,
        "alert": "on",
        "alert_count": 1,
        "unit_id": 0x001,
        "date": datetime.strptime("2013/1/22 11:38:23",
                                  '%Y/%m/%d %H:%M:%S')
    }),
    ('OK devstatus error "err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"',
        {
            "type": "ERROR",
            "message": "DCP[0] communication error",
            "alert_id": 0x53,
            "alert": "on",
            "alert_count": 1,
            "unit_id": 0x001,
            "date": datetime.strptime("2013/1/22 11:38:23",
                                      '%Y/%m/%d %H:%M:%S')
        }
     )
]

testdata_EventLogGetLogNumber = [
    ('OK event MTX:EventLogGetLogNumber "lognum=6"', 6)
]

testdata_EventLogGetLog = [
    ('OK event MTX:EventLogGetLog "log2=err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"',
        {
            "type": "ERROR",
            "message": "DCP[0] communication error",
            "alert_id": 0x53,
            "alert": "on",
            "alert_count": 1,
            "unit_id": 0x001,
            "date": datetime.strptime("2013/1/22 11:38:23",
                                      '%Y/%m/%d %H:%M:%S')
        })
]

testdata_EventLogGetLogList = [
    ('OK event MTX:EventLogGetLogList logindex=0-5|log0=err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23|log1=flt/System error// x01 on ….', [
     'err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23', 'flt/System error// x01 on ….'])
]


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_error_type_field(input_str, expected):
    """[summary]

    [description]

    Decorators:
        pytest.mark.parametrize

    Arguments:
        input_str {[type]} -- [description]
        expected {[type]} -- [description]
    """
    result = parse_devstatus_error(input_str)
    assert 'type' in result


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_error_type(input_str, expected):
    """[summary]

    [description]

    Decorators:
        pytest.mark.parametrize

    Arguments:
        input_str {[type]} -- [description]
        expected {[type]} -- [description]
    """
    result = parse_devstatus_error(input_str)
    assert result['type'] == expected['type']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_error_type_value(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['type'] in ['', 'FAULT', 'ERROR', 'WARNING']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_error_message_field(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert 'message' in result


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_error_message_value(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['message'] == expected['message']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_error_message_length(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert len(result['message']) <= 32


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_error_message_ascii(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['message'].isascii()


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_alert_id_field(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert 'alert_id' in result


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_alert_id_value(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['alert_id'] == expected['alert_id']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_alert_id_digit_length(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert 15 < result['alert_id']
    assert 4095 > result['alert_id']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_alert_count_field(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert 'alert_count' in result


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_alert_count_int(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert int("%s" % result['alert_count'], 10) == expected['alert_count']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_alert_count_len(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['alert_count'] <= 99999


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_alert_count_value(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['alert_count'] == expected['alert_count']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_unit_id_field(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert 'unit_id' in result


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_unit_id_len(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['unit_id'] <= 4095


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_unit_id(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['unit_id'] == expected['unit_id']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_date(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert 'date' in result


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_date_value(input_str, expected):
    result = parse_devstatus_error(input_str)
    assert result['date'] == expected['date']


@pytest.mark.parametrize("input_str, expected", testdata_devstatus_error)
def test_devstatus_date_diff(input_str, expected):
    result = parse_devstatus_error(input_str)
    diff = result['date'] - expected['date']
    assert diff == timedelta(0)


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLogNumber)
def test_EventLogGetLogNumber(input_str, expected):
    result = parse_EventLogGetLogNumber(input_str)
    assert result == expected


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLogNumber)
def test_EventLogGetLogNumber_int(input_str, expected):
    result = parse_EventLogGetLogNumber(input_str)
    assert int(result) == int(expected)


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert result == expected


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_type_field(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert 'type' in result


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_type_value(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert result['type'] == expected['type']


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_message_field(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert 'message' in result


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_message_value(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert result['message'] == expected['message']


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_message_length(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert len(result['message']) <= 32


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_message_ascii(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert result['message'].isascii()


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_alert_id_field(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert 'alert_id' in result


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_alert_id_value(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert result['alert_id'] == expected['alert_id']


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_alert_count_field(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert 'alert_count' in result


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_alert_count_value(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert result['alert_count'] == expected['alert_count']


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_unit_id_field(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert 'unit_id' in result


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_unit_id_value(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert result['unit_id'] == expected['unit_id']


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_date_field(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert 'date' in result


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_date_value(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    assert result['date'] == expected['date']


@pytest.mark.parametrize("input_str, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_date_dt(input_str, expected):
    result = parse_EventLogGetLog(input_str)
    diff = result['date'] - expected['date']
    assert timedelta(0) == diff


@pytest.mark.parametrize("input_str, expected", testdata_match_replace)
def test_match_replace(input_str, expected):
    result = match_replace(input_str, expected['needle'])
    assert result == expected['result']
