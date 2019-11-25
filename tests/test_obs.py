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

import os
import shutil
import tempfile
import unittest

import lsst.utils
import lsst.utils.tests

TESTDIR = os.path.abspath(os.path.dirname(__file__))
executable_dir = os.path.join(TESTDIR, os.path.pardir, "scripts")


class ExampleObsTestCase(lsst.utils.tests.ExecutablesTestCase):
    """Test an example obs_ processing run."""

    def setUp(self):
        self.root = tempfile.mkdtemp(dir=TESTDIR)
        # The test scripts themselves do not yet have the ability
        # to specify an output directory so we change directory here.
        self.cwd = os.getcwd()
        os.chdir(self.root)

        # Track test failure
        self.failed = False

    def tearDown(self):
        os.chdir(self.cwd)
        if self.root is not None and os.path.exists(self.root):
            # Clean up the test data unless there was a failure.
            if self.failed:
                print(f"Output test data located in {self.root}")
            else:
                shutil.rmtree(self.root, ignore_errors=True)

    def testObsCfhtQuick(self):
        """Test obs_cfht"""
        try:
            self.assertExecutable("runCfhtQuickTest.sh",
                                  root_dir=executable_dir,
                                  args=["--", "--noplot"],
                                  msg="CFHT Quick Test failed")
        except AssertionError:
            self.failed = True
            raise

    def testObsDecamQuick(self):
        """Test obs_decam"""
        try:
            self.assertExecutable("runDecamQuickTest.sh",
                                  root_dir=executable_dir,
                                  args=["--", "--noplot"],
                                  msg="DECam Quick Test failed")
        except AssertionError:
            self.failed = True
            raise


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
