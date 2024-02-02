class AdvocateException(Exception):
    pass


class UnacceptableAddressException(AdvocateException):
    pass


class UnacceptableRequestException(AdvocateException):
    pass


class NameserverException(AdvocateException):
    pass


class MountDisabledException(AdvocateException):
    pass


class ProxyDisabledException(NotImplementedError, AdvocateException):
    pass


class ConfigException(AdvocateException):
    pass
