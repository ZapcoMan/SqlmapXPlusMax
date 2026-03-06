#!/usr/bin/env python

"""
Copyright (c) 2006-2024 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from lib.core.data import logger
from plugins.generic.takeover import Takeover as GenericTakeover

class Takeover(GenericTakeover):
    def osShell(self):
        warnMsg = "on Spark SQL it is not possible to execute operating system commands"
        logger.warning(warnMsg)

        return None

    def osPwn(self):
        warnMsg = "on Spark SQL it is not possible to establish an out-of-band connection"
        logger.warning(warnMsg)

        return None

    def osSmb(self):
        warnMsg = "on Spark SQL it is not possible to establish SMB connection"
        logger.warning(warnMsg)

        return None

    def osBof(self):
        warnMsg = "on Spark SQL it is not possible to execute buffer overflow"
        logger.warning(warnMsg)

        return None
