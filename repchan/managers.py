# -*- encoding: utf-8

from django.db import models
from django.db.models.query import QuerySet

class RawManager(models.Manager):
    '''
    The original manager django.
    '''
    pass

class VersionManager(models.Manager):
    '''
    Manager version history.
    '''

    def get_query_set(self):
        return super(VersionManager, self).get_query_set()

    def get_all_revisions_for(self, main_version):
        return self.get_query_set().filter(version_parent_pk=main_version,
                                           version_unique_on__isnull=False)

    def get_next_revisions(self, revision):
        return self.get_query_set().filter(version_parent_rev_pk=revision,
                                           version_unique_on__isnull=False)

class VersionQuerySet(models.query.QuerySet):

    def delete(self, hard=False, *args, **kwargs):
        # removed from the database or move to trash
        if self.version_in_trash or hard:
            # without sending signals post_delete, pre_delete
            super(VersionQuerySet, self).delete(*args, **kwargs)
        elif hard:
            # with sending signals
            signal_allow(self, models.signals.pre_delete)
            signal_allow(self, models.signals.post_delete)

            super(VersionQuerySet, self).delete(*args, **kwargs)

            signal_allow(self, models.signals.pre_delete, count=0)
            signal_allow(self, models.signals.post_delete, count=0)
        else:
            pass
        # TODO: QuerySet.delete collector
        # TODO: Disable delete context


class DefaultManager(models.Manager):
    '''
    The default manager.
    '''
    #use_for_related_fields = True # WARNING: errors

    def get_query_set(self):
        return VersionQuerySet(self.model, using=self._db).\
                        filter(version_in_trash=False, version_unique_on=False)

    def in_trash(self):
        '''
        list of objects in the trash
        '''
        return super(DefaultManager, self).get_query_set().\
                        filter(version_in_trash=True, version_unique_on=False)

    def together_with_trash(self):
        '''
        list of objects in the trash
        '''
        return super(DefaultManager, self).get_query_set().\
                        filter(version_unique_on=False)

