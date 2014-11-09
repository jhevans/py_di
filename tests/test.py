from unittest.case import TestCase

from py_di.injector import Injector, MissingFeatureException, DuplicateFeatureException, NotCallableException


__author__ = 'JohnH.Evans'


class InjectorTest(TestCase):
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
        Injector().remove_all_features()

    def test_exception_raised_for_unavailable_feature(self):
        with self.assertRaises(MissingFeatureException) as context_manager:
            Injector().get_feature('foo')
        self.assertEqual(context_manager.exception.message, "Feature 'foo' has not been provided")

    def test_feature_returned_when_provided_with_class(self):
        Injector().provide('foo', self.TestFeature)
        feature = Injector().get_feature('foo')

        self.assertEqual(type(feature), self.TestFeature)

    def test_feature_returned_when_provided_with_function(self):
        Injector().provide('foo', lambda: 'bar')
        feature = Injector().get_feature('foo')

        self.assertEqual(feature, 'bar')

    def test_exception_raised_when_non_callable_provided(self):
        with self.assertRaises(NotCallableException) as context_manager:
            Injector().provide('foo', 12345)
        self.assertEqual(context_manager.exception.message,
                         "Feature 'foo' of type <type 'int'> is not a callable object")

    def test_args_passed_to_feature(self):
        Injector().provide('foo', self.TestFeature, *('bar', 'baz'))
        self.assertEqual(Injector().get_feature('foo').args, ('bar', 'baz'))

    def test_kwargs_passed_to_feature(self):
        Injector().provide('foo', self.TestFeature, **{'bar': 1, 'baz': 2})
        self.assertEqual(Injector().get_feature('foo').kwargs, {'bar': 1, 'baz': 2})

    def test_remove_feature(self):
        Injector().provide('foo', self.TestFeature)
        Injector().remove_feature('foo')
        with self.assertRaises(MissingFeatureException):
            Injector().get_feature('foo')

    def test_get_features(self):
        Injector().provide('feature_1', self.TestFeature)
        Injector().provide('feature_2', self.TestFeature2)

        features = Injector().get_features()
        self.assertIn('feature_1', features)
        self.assertIn('feature_2', features)

        self.assertEqual(type(features['feature_1']), self.TestFeature)
        self.assertEqual(type(features['feature_2']), self.TestFeature2)

    def test_get_feature_names(self):
        for name in self.feature_names:
            Injector().provide(name, self.TestFeature)

        features = Injector().get_feature_names()

        self.assertEqual(features, sorted(self.feature_names))

    def test_remove_all_features(self):
        for name in self.feature_names:
            Injector().provide(name, self.TestFeature)

        Injector().remove_all_features()

        for name in self.feature_names:
            with self.assertRaises(MissingFeatureException):
                Injector().get_feature(name)

    def test_cant_duplicate_feature(self):
        Injector().provide('foo', self.TestFeature)
        with self.assertRaises(DuplicateFeatureException) as context_manager:
            Injector().provide('foo', self.TestFeature)
        self.assertEqual(context_manager.exception.message, "Feature 'foo' has already been provided")