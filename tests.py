#!/bin/env python3

from main import parse_devstatus_error, parse_EventLogGetLogNumber, parse_EventLogGetLog
import pytest
from datetime import datetime, timedelta

testdata_devstatus_error = [
    ('OK devstatus error "none"', {
        "type": "",
        "message": "",
        "alert_id": 0x10,
        "alert": "off",
        "alert_count": 0,
        "unit_id": 0x100,
        "date": datetime(1970,1,1,0,0,0)
    }),
    ('OK devstatus error "flt/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"', {
            "type": "FAULT",
            "message": "DCP[0] communication error",
            "alert_id": 0x53,
            "alert": "on",
            "alert_count": 1,
            "unit_id": 0x001,
            "date": datetime.strptime("2013/1/22 11:38:23", '%Y/%m/%d %H:%M:%S')
        }),
    ('OK devstatus error "err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"', {
            "type": "ERROR",
            "message": "DCP[0] communication error",
            "alert_id": 0x53,
            "alert": "on",
            "alert_count": 1,
            "unit_id": 0x001,
            "date": datetime.strptime("2013/1/22 11:38:23", '%Y/%m/%d %H:%M:%S')
        }),
    ('OK devstatus error "wrn/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"', {
            "type": "WARNING",
            "message": "DCP[0] communication error",
            "alert_id": 0x53,
            "alert": "on",
            "alert_count": 1,
            "unit_id": 0x001,
            "date": datetime.strptime("2013/1/22 11:38:23", '%Y/%m/%d %H:%M:%S')
        }),
    ('OK devstatus error "err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"',
        {
            "type": "ERROR",
            "message": "DCP[0] communication error",
            "alert_id": 0x53,
            "alert": "on",
            "alert_count": 1,
            "unit_id": 0x001,
            "date": datetime.strptime("2013/1/22 11:38:23", '%Y/%m/%d %H:%M:%S')
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
            "date": datetime.strptime("2013/1/22 11:38:23", '%Y/%m/%d %H:%M:%S')
        })
]

testdata_EventLogGetLogList = [
    ('OK event MTX:EventLogGetLogList logindex=0-5|log0=err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23|log1=flt/System error// x01 on ….', [
     'err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23', 'flt/System error// x01 on ….'])
]


@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_error_type_field(input, expected):
    """[summary]
    
    [description]
    
    Decorators:
        pytest.mark.parametrize
    
    Arguments:
        input {[type]} -- [description]
        expected {[type]} -- [description]
    """
    result = parse_devstatus_error(input)
    assert 'type' in result


@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_error_type(input, expected):
    """[summary]
    
    [description]
    
    Decorators:
        pytest.mark.parametrize
    
    Arguments:
        input {[type]} -- [description]
        expected {[type]} -- [description]
    """
    result = parse_devstatus_error(input)
    assert result['type'] == expected['type']


@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_error_type_value(input, expected):
    result = parse_devstatus_error(input)
    assert result['type'] in ['', 'FAULT', 'ERROR', 'WARNING']

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_error_message_field(input, expected):
    result = parse_devstatus_error(input)
    assert 'message' in result

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_error_message_value(input, expected):
    result = parse_devstatus_error(input)
    assert result['message'] == expected['message']

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_error_message_length(input, expected):
    result = parse_devstatus_error(input)
    assert len(result['message']) <= 32

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_error_message_ascii(input, expected):
    result = parse_devstatus_error(input)
    assert result['message'].isascii()

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_alert_id_field(input, expected):
    result = parse_devstatus_error(input)
    assert 'alert_id' in result

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_alert_id_field(input, expected):
    result = parse_devstatus_error(input)
    assert result['alert_id'] == expected['alert_id']


@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_alert_id_digit_length(input, expected):
    result = parse_devstatus_error(input)
    assert  15 < result['alert_id']
    assert  4095 > result['alert_id']

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_alert_count_field(input, expected):
    result = parse_devstatus_error(input)
    assert 'alert_count' in result

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_alert_count_int(input, expected):
    result = parse_devstatus_error(input)
    assert int("%s" % result['alert_count'], 10) == expected['alert_count']

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_alert_count_len(input, expected):
    result = parse_devstatus_error(input)
    assert len(result['alert_count']) <= 5

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_alert_count_len(input, expected):
    result = parse_devstatus_error(input)
    assert result['alert_count'] == expected['alert_count']

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_unit_id_field(input, expected):
    result = parse_devstatus_error(input)
    assert 'unit_id' in result

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_unit_id_len(input, expected):
    result = parse_devstatus_error(input)
    assert result['unit_id'] <= 4095

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_unit_id(input, expected):
    result = parse_devstatus_error(input)
    assert result['unit_id'] == expected['unit_id']

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_date(input, expected):
    result = parse_devstatus_error(input)
    assert 'date' in result

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_date_value(input, expected):
    result = parse_devstatus_error(input)
    assert result['date'] == expected['date']

@pytest.mark.parametrize("input, expected", testdata_devstatus_error)
def test_devstatus_date_diff(input, expected):
    result = parse_devstatus_error(input)
    diff = result['date'] - expected['date']
    assert diff == timedelta(0)


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLogNumber)
def test_EventLogGetLogNumber(input, expected):
    result = parse_EventLogGetLogNumber(input)
    assert result == expected


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLogNumber)
def test_EventLogGetLogNumber_int(input, expected):
    result = parse_EventLogGetLogNumber(input)
    assert int(result) == int(expected)


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog(input, expected):
    result = parse_EventLogGetLog(input)
    assert result == expected


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_type_field(input, expected):
    result = parse_EventLogGetLog(input)
    assert 'type' in result


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_type_value(input, expected):
    result = parse_EventLogGetLog(input)
    assert result['type'] == expected['type']


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_message_field(input, expected):
    result = parse_EventLogGetLog(input)
    assert 'message' in result


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_message_value(input, expected):
    result = parse_EventLogGetLog(input)
    assert result['message'] == expected['message']

@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_message_length(input, expected):
    result = parse_EventLogGetLog(input)
    assert len(result['message']) <= 32

@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_message_ascii(input, expected):
    result = parse_EventLogGetLog(input)
    assert result['message'].isascii()


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_alert_id_field(input, expected):
    result = parse_EventLogGetLog(input)
    assert 'alert_id' in result


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_alert_id_value(input, expected):
    result = parse_EventLogGetLog(input)
    assert result['alert_id'] == expected['alert_id']


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_alert_count_field(input, expected):
    result = parse_EventLogGetLog(input)
    assert 'alert_count' in result


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_alert_count_value(input, expected):
    result = parse_EventLogGetLog(input)
    assert result['alert_count'] == expected['alert_count']


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_unit_id_field(input, expected):
    result = parse_EventLogGetLog(input)
    assert 'unit_id' in result


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_unit_id_value(input, expected):
    result = parse_EventLogGetLog(input)
    assert result['unit_id'] == expected['unit_id']


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_date_field(input, expected):
    result = parse_EventLogGetLog(input)
    assert 'date' in result


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_date_value(input, expected):
    result = parse_EventLogGetLog(input)
    assert result['date'] == expected['date']


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_date_value(input, expected):
    result = parse_EventLogGetLog(input)
    assert result['date'] == expected['date']


@pytest.mark.parametrize("input, expected", testdata_EventLogGetLog)
def test_EventLogGetLog_date_dt(input, expected):
    result = parse_EventLogGetLog(input)
    diff = result['date'] - expected['date']
    assert timedelta(0) == diff
