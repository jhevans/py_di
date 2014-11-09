__author__ = 'JohnH.Evans'

import os
from unittest.case import TestCase

from py_di import injector


# This has to be tested separately as the singleton model enforces that automatic provisioning can only happen once
class TestAutoImport(TestCase):
    def test_provisioning_sanity_test(self):
        os.environ['PY_DI_PROVISIONING_MODULE'] = 'py_di_provisioning'
        self.assertEqual(injector.Injector().get_feature('auto_imported_feature'), 'ok')