# -*- encoding: utf-8

from django.db import models

class RawManager(models.Manager):
    '''
    The original manager django.
    '''
    pass

class VersionManager(models.Manager):
    '''
    Manager version history.
    '''

    def heads_list(self):
        pass


class DefaultManager(models.Manager):
    '''
    The default manager.
    '''
    #use_for_related_fields = True # WARNING: errors

    def get_query_set(self):
        return super(DefaultManager, self).get_query_set().\
                        filter(version_in_trash=False, version_unique_on=False)

    def in_trash(self):
        '''
        list of objects in the trash
        '''
        return super(DefaultManager, self).get_query_set().\
                        filter(version_in_trash=True, version_unique_on=False)
