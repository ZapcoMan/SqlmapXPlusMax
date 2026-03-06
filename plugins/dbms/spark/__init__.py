#!/usr/bin/env python

"""
Copyright (c) 2006-2024 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from lib.core.enums import DBMS
from lib.core.settings import SPARK_SYSTEM_DBS
from lib.core.unescaper import unescaper

from plugins.dbms.spark.enumeration import Enumeration
from plugins.dbms.spark.filesystem import Filesystem
from plugins.dbms.spark.fingerprint import Fingerprint
from plugins.dbms.spark.syntax import Syntax
from plugins.dbms.spark.takeover import Takeover
from plugins.generic.misc import Miscellaneous

class SparkMap(Syntax, Fingerprint, Enumeration, Filesystem, Miscellaneous, Takeover):
    """
    This class defines Spark SQL methods
    """

    def __init__(self):
        self.excludeDbsList = SPARK_SYSTEM_DBS

        for cls in self.__class__.__bases__:
            cls.__init__(self)

    unescaper[DBMS.SPARK] = Syntax.escape
