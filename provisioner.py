__author__ = 'JohnH.Evans'


class ProvisioningError(BaseException):
    message_template = "Unable to provision resource %s"

    def __init__(self, resource):
        super(ProvisioningError, self).__init__(self.message_template % resource)


class Provisioner(object):
    instance = None

    class __ProvisionerSingleton(object):
        provisions = {}

        def __init__(self):
            pass

        def get_dependency(self, dependency):
            return self.provisions[dependency]

        def provision(self, dependency, cls):
            try:
                self.provisions[dependency] = cls()
            except KeyError:
                raise ProvisioningError(dependency)

    def __init__(self):
        if self.instance:
            self.instance
        else:
            self.instance = self.__ProvisionerSingleton()

    def __getattr__(self, name):
        return getattr(self.instance, name)
