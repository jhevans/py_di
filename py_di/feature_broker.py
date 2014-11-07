__author__ = 'JohnH.Evans'


class MissingFeatureException(BaseException):
    message_template = "Feature '%s' has not been provided"

    def __init__(self, feature):
        super(MissingFeatureException, self).__init__(self.message_template % feature)


class DuplicateFeatureException(BaseException):
    message_template = "Feature '%s' has already been provided"

    def __init__(self, feature):
        super(DuplicateFeatureException, self).__init__(self.message_template % feature)


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
            try:
                self.features[feature_name]
                raise DuplicateFeatureException(feature_name)
            except KeyError:
                self.features[feature_name] = cls()

        def remove_feature(self, feature_name):
            del self.features[feature_name]

        def get_feature_names(self):
            return sorted(self.features.keys())

        def get_features(self):
            return sorted(self.features.items())

        def remove_all_features(self):
            self.features = {}


    def __init__(self):
        if not FeatureBroker.instance:
            FeatureBroker.instance = FeatureBroker.__FeatureBrokerSingleton()

    def __getattr__(self, name):
        return getattr(FeatureBroker.instance, name)

    # All functionality should be provided in the __FeatureBrokerSingleton class, these methods are provided only so
    # that IDE auto complete works.
    @staticmethod
    def get_feature(feature_name):
        return FeatureBroker.instance.get_feature(feature_name)

    @staticmethod
    def provide(feature_name, cls):
        return FeatureBroker.instance.provide(feature_name, cls)
