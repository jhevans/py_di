__author__ = 'JohnH.Evans'


class MissingFeatureException(BaseException):
    message_template = "Feature '%s' has not been provided"

    def __init__(self, resource):
        super(MissingFeatureException, self).__init__(self.message_template % resource)


class FeatureBroker(object):
    instance = None

    class __FeatureBrokerSingleton(object):
        features = {}

        def __init__(self):
            pass

        def get_feature(self, feature_name):
            try:
                return self.features[feature_name]
            except KeyError:
                raise MissingFeatureException(feature_name)

        def provide(self, feature_name, cls):
            self.features[feature_name] = cls()

    def __init__(self):
        if self.instance:
            self.instance
        else:
            self.instance = self.__FeatureBrokerSingleton()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    # All functionality should be provided in the __FeatureBrokerSingleton class, these methods are provided only so
    # that IDE auto complete works.
    def get_feature(self, feature_name):
        return self.instance.get_feature(feature_name)

    def provide(self, feature_name, cls):
        return self.instance.provide(feature_name, cls)