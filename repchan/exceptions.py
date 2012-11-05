# -*- encoding: utf-8



class VersionException(Exception):
    pass


class VersionCommitException(VersionException):
    pass


class VersionReadOnlyException(VersionException):
    'Is thrown when an attribute of the model object is read-only.'
    pass


class VersionDisabledMethodException(VersionException):
    'For blocked methods.'
    pass




