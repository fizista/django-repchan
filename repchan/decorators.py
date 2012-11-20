# -*- encoding: utf-8
from repchan.exceptions import VersionDisabledMethodException

def enable_in_trash_context(method):
    'Disabling methods of context "main"'
    def decorator(self, *args, **kwargs):
        if self.check_is_main_version() and self.version_in_trash == True:
            raise VersionDisabledMethodException(
                                     'This method can be used only in the '
                                     'context of "trash".')
        else:
            return method(self, *args, **kwargs)
    return decorator

def disable_in_main_context(method):
    'Disabling methods of context "main"'
    def decorator(self, *args, **kwargs):
        if self.check_is_main_version():
            raise VersionDisabledMethodException(
                                     'This method can not be used in the '
                                     'context of "main".')
        else:
            return method(self, *args, **kwargs)
    return decorator


def disable_in_revision_context(method):
    'Disabling methods of context "revision"'
    def decorator(self, *args, **kwargs):
        if self.check_is_revision():
            raise VersionDisabledMethodException(
                                     'This method can not be used in the '
                                     'context of "revision".')
        else:
            return method(self, *args, **kwargs)
    return decorator


def disable_in_revision_new_context(method):
    'Disabling methods of context "revision new"'
    def decorator(self, *args, **kwargs):
        if self.check_is_revision_new():
            raise VersionDisabledMethodException(
                                     'This method can not be used in the '
                                     'context of "revision new".')
        else:
            return method(self, *args, **kwargs)
    return decorator

