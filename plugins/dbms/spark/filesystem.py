#!/usr/bin/env python

"""
Copyright (c) 2006-2024 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from lib.core.data import logger
from plugins.generic.filesystem import Filesystem as GenericFilesystem

class Filesystem(GenericFilesystem):
    def readFile(self, rFile):
        warnMsg = "on Spark SQL it is not possible to read files"
        logger.warning(warnMsg)

        return None

    def writeFile(self, wFile, dFile, fileType=None, forceCheck=False):
        warnMsg = "on Spark SQL it is not possible to write files"
        logger.warning(warnMsg)

        return False

    def stackedReadFile(self, rFile):
        warnMsg = "on Spark SQL it is not possible to read files"
        logger.warning(warnMsg)

        return None
