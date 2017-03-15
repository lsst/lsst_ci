#
# LSST Data Management System
# Copyright 2012-2017 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

from __future__ import print_function

import os
import unittest

import lsst.utils
import lsst.utils.tests

executable_dir = os.path.join(
    lsst.utils.getPackageDir("VALIDATE_DRP"),
    "examples")

class ExampleObsTestCase(lsst.utils.tests.ExecutablesTestCase):
    """Test an example obs_ processing run."""
    def testObsCfhtQuick(self):
        """Test obs_cfht"""
        self.assertExecutable("runCfhtQuickTest.sh",
                              root_dir=executable_dir,
                              args=["--noplot"],
                              msg="CFHT Quick Test failed")

    def testObsDecamQuick(self):
        """Test obs_decam"""
        self.assertExecutable("runDecamQuickTest.sh",
                              root_dir=executable_dir,
                              args=["--noplot"],
                              msg="DECam Quick Test failed")


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
