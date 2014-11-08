from unittest.case import TestCase, skip

from py_di.feature_broker import FeatureBroker, MissingFeatureException, DuplicateFeatureException, NotAClassException


__author__ = 'JohnH.Evans'


class FeatureBrokerTest(TestCase):
    class TestFeature(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

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

    def test_args_passed_to_feature(self):
        FeatureBroker().provide('foo', self.TestFeature, *('bar', 'baz'))
        self.assertEqual(FeatureBroker().get_feature('foo').args, ('bar', 'baz'))

    def test_kwargs_passed_to_feature(self):
        FeatureBroker().provide('foo', self.TestFeature, **{'bar': 1, 'baz': 2})
        self.assertEqual(FeatureBroker().get_feature('foo').kwargs, {'bar': 1, 'baz': 2})

    def test_remove_feature(self):
        FeatureBroker().provide('foo', self.TestFeature)
        FeatureBroker().remove_feature('foo')
        with self.assertRaises(MissingFeatureException):
            FeatureBroker().get_feature('foo')

    @skip('this one is not a priority')
    def test_get_features(self):
        for index, name in enumerate(self.feature_names):
            if index % 2 == 0:
                FeatureBroker().provide(name, self.TestFeature)
            else:
                FeatureBroker().provide(name, self.TestFeature2)

        features = FeatureBroker().get_features()

        for index, name in enumerate(sorted(self.feature_names)):
            self.assertEqual(features[index][0], name)
            if index % 2 == 0:
                self.assertEqual(features[index][1], self.TestFeature)
            else:
                self.assertEqual(features[index][1], self.TestFeature2)

    def test_get_feature_names(self):
        for name in self.feature_names:
            FeatureBroker().provide(name, self.TestFeature)

        features = FeatureBroker().get_feature_names()

        self.assertEqual(features, sorted(self.feature_names))

    def test_remove_all_features(self):
        for name in self.feature_names:
            FeatureBroker().provide(name, self.TestFeature)

        FeatureBroker().remove_all_features()

        for name in self.feature_names:
            with self.assertRaises(MissingFeatureException):
                FeatureBroker().get_feature(name)

    def test_cant_duplicate_feature(self):
        FeatureBroker().provide('foo', self.TestFeature)
        with self.assertRaises(DuplicateFeatureException) as context_manager:
            FeatureBroker().provide('foo', self.TestFeature)
        self.assertEqual(context_manager.exception.message, "Feature 'foo' has already been provided")

    def test_provide_requires_callable(self):
        with self.assertRaises(NotAClassException) as context_manager:
            FeatureBroker().provide('foo', 12345)
        self.assertEqual(context_manager.exception.message, "Feature 'foo' is not a class")