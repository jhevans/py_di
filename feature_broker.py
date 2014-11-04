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

    # # These method stubs are provided only to allow IDE auto_completion
    # def get_feature(self, feature_name):
    #     assert False, 'This method should not be callable'
    #
    # def provide(self, feature_name, cls):
    #     assert False, 'This method should not be callable'
