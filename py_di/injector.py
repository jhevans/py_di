__author__ = 'JohnH.Evans'


class MissingFeatureException(BaseException):
    message_template = "Feature '%s' has not been provided"

    def __init__(self, feature):
        super(MissingFeatureException, self).__init__(self.message_template % feature)


class DuplicateFeatureException(BaseException):
    message_template = "Feature '%s' has already been provided"

    def __init__(self, feature):
        super(DuplicateFeatureException, self).__init__(self.message_template % feature)

class NotCallableException(BaseException):
    message_template = "Feature '%s' of type %s is not a callable object"

    def __init__(self, name, obj):
        super(NotCallableException, self).__init__(self.message_template % (name, str(type(obj))))

class Injector(object):
    __instance = None

    class __InjectorSingleton(object):
        features = {}

        def __init__(self):
            pass

        def get_feature(self, feature_name):
            try:
                return self.features[feature_name]
            except KeyError:
                raise MissingFeatureException(feature_name)

        def provide(self, feature_name, feature_callable, *args, **kwargs):
            if not hasattr(feature_callable, '__call__'):
                raise NotCallableException(feature_name, feature_callable)
            try:
                self.features[feature_name]
                raise DuplicateFeatureException(feature_name)
            except KeyError:
                self.features[feature_name] = feature_callable(*args, **kwargs)

        def remove_feature(self, feature_name):
            del self.features[feature_name]

        def get_feature_names(self):
            return sorted(self.features.keys())

        def get_features(self):
            return self.features.copy()

        def remove_all_features(self):
            self.features = {}


    def __init__(self):
        if not Injector.__instance:
            Injector.__instance = Injector.__InjectorSingleton()

    def __getattr__(self, name):
        return getattr(Injector.__instance, name)

    # All functionality should be provided in the __InjectorSingleton class, these methods are provided only so
    # that IDE auto complete works.
    @staticmethod
    def get_feature(feature_name):
        return Injector.__instance.get_feature(feature_name)

    @staticmethod
    def provide(feature_name, cls, *args, **kwargs):
        return Injector.__instance.provide(feature_name, cls, *args, **kwargs)
