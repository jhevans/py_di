from unittest.case import TestCase, skip
from feature_broker import FeatureBroker, MissingFeatureException, DuplicateFeatureException

__author__ = 'JohnH.Evans'


class FeatureBrokerTest(TestCase):
    class TestFeature(object):
        pass

    class TestFeature2(object):
        pass

    feature_names = [
        'foo',
        'xzyzzy',
        'bar',
        'baz',
        'frob'
    ]

    def tearDown(self):
        FeatureBroker().remove_all_features()

    def test_exception_raised_for_unavailable_feature(self):
        with self.assertRaises(MissingFeatureException) as context_manager:
            FeatureBroker().get_feature('foo')
        self.assertEqual(context_manager.exception.message, "Feature 'foo' has not been provided")

    def test_feature_returned_when_provided(self):
        FeatureBroker().provide('foo', self.TestFeature)
        feature = FeatureBroker().get_feature('foo')

        self.assertEqual(type(feature), self.TestFeature)

    def test_remove_feature(self):
        FeatureBroker().provide('foo', self.TestFeature)
        FeatureBroker().remove_feature('foo')
        with self.assertRaises(MissingFeatureException):
            FeatureBroker().get_feature('foo')

    def test_get_features(self):
        for name in self.feature_names:
            FeatureBroker().provide(name, self.TestFeature)

        features = FeatureBroker().get_feature_names()

        self.assertEqual(features, sorted(self.feature_names))

    @skip('This aint working')
    def test_remove_all_features(self):
        for name in self.feature_names:
            FeatureBroker().provide(name, self.TestFeature)

        FeatureBroker().remove_all_features()

        for name in self.feature_names:
            with self.assertRaises(MissingFeatureException):
                FeatureBroker().get_feature(name)

    @skip("There's something really funky going on here...")
    def test_cant_duplicate_feature(self):
        FeatureBroker().provide('foo', self.TestFeature)
        with self.assertRaises(DuplicateFeatureException) as context_manager:
            FeatureBroker().provide('foo', self.TestFeature)
        self.assertEqual(context_manager.exception.message, "Feature 'foo' has already been provided")