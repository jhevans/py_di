from unittest.case import TestCase
from mock import Mock
from feature_broker import FeatureBroker, MissingFeatureException

__author__ = 'JohnH.Evans'


class FeatureBrokerTest(TestCase):
    def test_exception_raised_for_unavailable_feature(self):
        with self.assertRaises(MissingFeatureException) as context_manager:
            FeatureBroker().get_feature('foo')
        self.assertEqual(context_manager.exception.message, "Feature 'foo' has not been provided")

    def test_feature_returned_when_provided(self):
        class TestFeature(object):
            pass
        FeatureBroker().provide('foo', TestFeature)
        feature = FeatureBroker().get_feature('foo')

        self.assertEqual(type(feature), TestFeature)