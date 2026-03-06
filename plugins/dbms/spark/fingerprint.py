#!/usr/bin/env python

"""
Copyright (c) 2006-2024 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from lib.core.common import Backend
from lib.core.common import Format
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import logger
from lib.core.enums import DBMS
from lib.core.session import setDbms
from lib.core.settings import SPARK_ALIASES
from lib.request import inject
from plugins.generic.fingerprint import Fingerprint as GenericFingerprint

class Fingerprint(GenericFingerprint):
    def __init__(self):
        GenericFingerprint.__init__(self, DBMS.SPARK)

    def getFingerprint(self):
        value = ""
        wsOsFp = Format.getOs("web server", kb.headersFp)

        if wsOsFp:
            value += "%s\n" % wsOsFp

        if kb.data.banner:
            dbmsOsFp = Format.getOs("back-end DBMS", kb.bannerFp)

            if dbmsOsFp:
                value += "%s\n" % dbmsOsFp

        value += "back-end DBMS: "

        if not conf.extensiveFp:
            value += DBMS.SPARK
            return value

        actVer = Format.getDbms()
        blank = " " * 15
        value += "active fingerprint: %s" % actVer

        if kb.bannerFp:
            banVer = kb.bannerFp.get("dbmsVersion")

            if banVer:
                banVer = Format.getDbms([banVer])
                value += "\n%sbanner parsing fingerprint: %s" % (blank, banVer)

        htmlErrorFp = Format.getErrorParsedDBMSes()

        if htmlErrorFp:
            value += "\n%shtml error message fingerprint: %s" % (blank, htmlErrorFp)

        return value

    def checkDbms(self):
        if not conf.extensiveFp and Backend.isDbmsWithin(SPARK_ALIASES):
            setDbms(DBMS.SPARK)

            self.getBanner()

            return True

        infoMsg = "testing %s" % DBMS.SPARK
        logger.info(infoMsg)
        
        # Spark SQL specific fingerprinting tests
        # Test 1: Check for Spark SQL specific function
        result = inject.checkBooleanExpression("current_database() IS NOT NULL")

        if result:
            infoMsg = "confirming %s" % DBMS.SPARK
            logger.info(infoMsg)
            
            # Test 2: Check for Spark SQL version function
            result = inject.checkBooleanExpression("version() IS NOT NULL")

            if not result:
                warnMsg = "the back-end DBMS is not %s" % DBMS.SPARK
                logger.warn(warnMsg)

                return False
            
            setDbms(DBMS.SPARK)
            self.getBanner()
            return True
        else:
            warnMsg = "the back-end DBMS is not %s" % DBMS.SPARK
            logger.warn(warnMsg)

            return False

    def forceDbmsEnum(self):
        # Force database enumeration for Spark SQL
        if conf.db:
            conf.db = conf.db.strip()
        
        return True
