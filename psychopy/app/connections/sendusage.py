#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the PsychoPy library
# Copyright (C) 2018 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

from __future__ import absolute_import, division, print_function
import time
import sys
import platform
import psychopy
from psychopy import web, logging
import requests


def sendUsageStats(app=None):
    """Sends anonymous, very basic usage stats to psychopy server:
      the version of PsychoPy
      the system used (platform and version)
      the date
    """

    v = psychopy.__version__
    dateNow = time.strftime("%Y-%m-%d_%H:%M")
    try:
        miscInfo = platform.machine()
    except AttributeError:
        miscInfo=''

    # get platform-specific info
    if sys.platform == 'darwin':
        OSXver, junk, architecture = platform.mac_ver()
        systemInfo = "OSX_%s" % (OSXver)
    elif sys.platform.startswith('linux'):
        systemInfo = '%s_%s_%s' % (
            'Linux',
            ':'.join([x for x in platform.dist() if x != '']),
            platform.release())
        if len(systemInfo) > 30:  # if it's too long PHP/SQL fails to store!?
            systemInfo = systemInfo[0:30]
    elif sys.platform == 'win32':
        systemInfo = "win32_v" + platform.version()
    else:
        systemInfo = platform.system() + platform.release()
    u = "https://usage.psychopy.org/submit.php?date=%s&sys=%s&version=%s&misc=%s"
    URL = u % (dateNow, systemInfo, v, miscInfo)
    try:
        req = web.urllib.request.Request(URL)
        page = web.urllib.request.urlopen(req)  # proxies
    except Exception:
        logging.warning("Couldn't connect to psychopy.org\n"
                        "Check internet settings (and proxy "
                        "setting in PsychoPy Preferences.")
