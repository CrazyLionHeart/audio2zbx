#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the MIT license.
"""[summary]

[description]
"""

import logging
import re
import sys
import telnetlib
import threading
from datetime import datetime
from os import getenv, unsetenv


def read_env(var, default=None):
    """[summary]

    [description]

    Arguments:
        var {[type]} -- [description]

    Keyword Arguments:
        default {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """
    result = getenv(var, default)
    LOG.debug("%s: %s", var, result)
    LOG.debug("Cleaning env %s", var)
    unsetenv(var)
    return result


def config_logging():
    """Configure base logging

    Function set default logging level and configure outut to stdout

    Returns:
        logging -- configured loggger
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s")

    zabbix_handler = logging.StreamHandler(sys.stdout)
    zabbix_handler.setFormatter(formatter)
    root_logger.addHandler(zabbix_handler)
    return root_logger


def parse_devstatus_error(input_str):
    """Parse command `devstatus error` output

    Функция принимает на вход ответ от команды `devstatus error` и преобразует его в словарь

    Arguments:
        input_str {str} -- Ответ от устройства:

        `OK devstatus error "err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23"`

    Returns:
        dict -- parsed result

        `
            {
                "type": flt = fault, err = error, wrn = warning
                "message": Maximum 32 letter (ascii character)
                "alert_id": nnn - 2 or 3 digit hexadecimal
                "alert": Alert on/off. Persistent alerts turn on when an alert condition occurs and turn off when they are cleared. Single-shot alerts turn on while an alert condition is true
                "alert_count": sssss
                "unit_id": xxx - 3 digit hexadecimal
                "date": datetime(2013, 1, 22, 11, 38, 23)  # 2013/1/22 11:38:23
            }
        `
    """
    logging.debug(input_str)
    cmd = 'devstatus error'
    result = {
        "type": "",
        "message": "",
        "alert_id": 0x10,
        "alert": "off",
        "alert_count": 0,
        "unit_id": 0x100,
        "date": datetime(1970, 1, 1, 0, 0, 0)
    }

    input_list = input_str.split('"')[:-1]
    command_result = input_list[0].rstrip(cmd).strip()
    output = input_list[1]

    if output == 'none':
        return result

    match_keys = []
    match_result = {}
    # err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23
    regex = r'(?P<type>\w{3})/(?P<message>.{0,32})//\s(?P<alert_id>x\d{2,3})\s(?P<alert>\w{2,3})\s\((?P<alert_count>\d{1,5})\)\sID-(?P<unit_id>\d{3})\s(?P<date>\d{4}/\d{1,2}/\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})'

    for match in re.finditer(regex, output):
        match_keys = match.re.groupindex.keys()
        match_result = match.groupdict()

    for key in match_keys:
        if key in result:
            result[key] = match_result[key]
            if key == 'type':
                if result[key] == 'none':
                    result[key] = ""
                elif result[key] == 'flt':
                    result[key] = "FAULT"
                elif result[key] == 'err':
                    result[key] = "ERROR"
                elif result[key] == 'wrn':
                    result[key] = "WARNING"
            if key == 'alert_count':
                result[key] = int(result[key])
            if key == 'alert_id':
                result[key] = int('0%s' % result[key], 16)
            if key == 'unit_id':
                result[key] = int('0x%s' % result[key], 16)
            if key == 'date':
                result[key] = datetime.strptime(
                    result[key], '%Y/%m/%d %H:%M:%S')

    return result


def parse_EventLogGetLogNumber(input_str):
    """[summary]

    [description]

    Arguments:
        input_str {str} -- [description]

        `
        OK event MTX:EventLogGetLogNumber "lognum=6"
        `

    Returns:
        int -- [description]
    """
    logging.debug(input_str)
    result = -1
    cmd = 'event MTX:EventLogGetLogNumber'
    input_list = input_str.split('"')[:-1]
    command_result = input_list[0].rstrip(cmd).strip()
    output = input_list[1]
    output_list = output.split('=')
    if len(output_list) == 2:
        result = int(output_list[1])
    return result


def parse_EventLogGetLog(input_str):
    """[summary]

    [description]

    Arguments:
        input_str {str} -- [description]

    Returns:
        dict -- [description]
    """
    logging.debug(input_str)
    cmd = 'event MTX:EventLogGetLog'
    result = {
        "type": "",
        "message": "",
        "alert_id": 0x10,
        "alert": "off",
        "alert_count": 0,
        "unit_id": 0x100,
        "date": datetime(1970, 1, 1, 0, 0, 0)
    }

    input_list = input_str.split('"')[:-1]
    command_result = input_list[0].rstrip(cmd).strip()
    output = input_list[1]

    if output == 'none':
        return result

    match_keys = []
    match_result = {}
    # err/DCP[0] communication error// x53 on (1) ID-001 2013/1/22 11:38:23
    regex = r'(?P<type>\w{3})/(?P<message>.{0,32})//\s(?P<alert_id>x\d{2,3})\s(?P<alert>\w{2,3})\s\((?P<alert_count>\d{1,5})\)\sID-(?P<unit_id>\d{3})\s(?P<date>\d{4}/\d{1,2}/\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})'

    for match in re.finditer(regex, output):
        match_keys = match.re.groupindex.keys()
        match_result = match.groupdict()

    for key in match_keys:
        if key in result:
            result[key] = match_result[key]
            if key == 'type':
                if result[key] == 'none':
                    result[key] = "None"
                elif result[key] == 'flt':
                    result[key] = "FAULT"
                elif result[key] == 'err':
                    result[key] = "ERROR"
                elif result[key] == 'wrn':
                    result[key] = "WARNING"
            if key == 'alert_count':
                result[key] = int(result[key])
            if key == 'alert_id':
                result[key] = int('0%s' % result[key], 16)
            if key == 'unit_id':
                result[key] = int('0x%s' % result[key], 16)
            if key == 'date':
                result[key] = datetime.strptime(
                    result[key],
                    '%Y/%m/%d %H:%M:%S'
                )

    return result


class Yamaha(object):
    """[summary]

    [description]
    """

    def __init__(self, host, port=49280):
        """[summary]

        [description]

        Arguments:
            host {[type]} -- [description]

        Keyword Arguments:
            port {number} -- [description] (default: {49280})
        """
        self.conn = telnetlib.Telnet(host, port)

    def _command(self, cmd):
        """[summary]

        [description]

        Arguments:
            cmd {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        self.conn.write(cmd)
        answer = self.conn.read_all()
        return str(answer)

    def get_EventLogGetLog(self, idx):
        """[summary]

        [description]

        Arguments:
            idx {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        cmd = 'event MTX:EventLogGetLog "logindex=%s"' % idx
        unparsed = self._command(cmd)
        parsed = parse_EventLogGetLog(unparsed)
        return parsed

    def get_EventLogGetLogNumber(self):
        """[summary]

        [description]

        Returns:
            [type] -- [description]
        """
        cmd = 'event MTX:EventLogGetLogNumber ""'
        unparsed = self._command(cmd)
        parsed = parse_EventLogGetLogNumber(unparsed)
        return parsed

    def get_devstatus_error(self):
        """[summary]

        [description]

        Returns:
            [type] -- [description]
        """
        cmd = 'devstatus error'
        unparsed = self._command(cmd)
        parsed = parse_devstatus_error(unparsed)
        return parsed


if __name__ == "__main__":

    LOG = config_logging()

    WAIT_TIME_SECONDS = int(read_env("WAIT_TIME_SECONDS", 60))
    ZABBIX_HOST = read_env("ZBX_HOST")
    ZABBIX_LOGIN = read_env("ZBX_USER")
    ZABBIX_PASSWD = read_env("ZBX_PASSWD")

    TICKER = threading.Event()
    while not TICKER.wait(WAIT_TIME_SECONDS):
        pass
