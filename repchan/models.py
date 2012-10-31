# -*- encoding: utf-8
import datetime
import hashlib
import inspect

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc
from django.db.models import F
from django.db import router
from django.db.models.deletion import Collector

from repchan.managers import VersionManager, RawManager, DefaultManager
from repchan.signals import revision_post_commit, revision_post_create, \
                            revision_set_as_main, signal_send_on, \
                            signal_send_off, signal_send_mask, signal_allow


NULL_DATE = datetime.datetime(1991, 12, 21).replace(tzinfo=utc)

# enable masking signal
signal_send_mask(models.signals.pre_save)
signal_send_mask(models.signals.post_save)

signal_send_mask(models.signals.pre_delete)
signal_send_mask(models.signals.post_delete)



class Value(object):

    def data_from_main_to_revision(self, obj_main, obj_revision, field_name):
        raise NotImplementedError('data_from_main_to_revision')

    def data_from_revision_to_main(self, obj_revision, obj_main, field_name):
        raise NotImplementedError('data_from_revision_to_main')

    def data_from_revision_to_revision(self, obj_revision_from,
                                            obj_revision_to, field_name):
        raise NotImplementedError('data_from_revision_to_revision')


class ValueStandardException(Exception):
    pass


class ValueStandard(Value):
    '''
    Main value field = previous main value field
    Revision value field = value set in the initialization of an object or
                           default model value
    '''

    def __init__(self, default_value=None):
        self.default_value = default_value

    def _get_default_model_value(self, obj, field_name):
        '''
        return default model value
        
        raise ValueStandardException - when there is no default
        '''
        field = [f for f in obj._meta._fields() if f.attname == field_name ][0]
        if field.has_default():
            return field.default
        else:
            raise ValueStandardException('The field does not have a default '
                                         'value.')

    def _get_default(self):
        if self.default_value:
            return self.default_value
        else:
            try:
                return _get_default_model_value(obj_main)
            except ValueStandardException:
                raise

    def data_from_main_to_revision(obj_main, obj_revision, field_name):
        return self._get_default()

    def data_from_revision_to_main(obj_revision, obj_main, field_name):
        return getattr(obj_main, field_name)

    def data_from_revision_to_revision(obj_revision_from, obj_revision_to,
                                           field_name):
        return self._get_default()


def _get_current_date():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


class VersionException(Exception): pass
class VersionBranchException(VersionException): pass
class VersionCommitException(VersionException): pass

class VersionReadOnlyException(Exception): pass
class VersionRevisionCreateException(Exception): pass
class VersionDisabledMethodException(Exception): pass
class VersionSetAsMainException(Exception): pass


class VersionModelBase(models.base.ModelBase):
    '''
    attrs['__version_original_fields_names']
    '''
    def __new__(cls, name, bases, attrs):

        # Get all the parents of the class
        parents = [b for b in bases if isinstance(b, VersionModelBase)]
        if not parents:
            # If this isn't a subclass of VersionModelBase, 
            # don't do anything special.
            return super(VersionModelBase, cls). \
                        __new__(cls, name, bases, attrs)

        # ############################
        # Get Versioning options
        # ############################
        def get_versioning_defaults():
            '''
            Seeking a default configuration for versioning
            '''
            for base in bases:
                options = getattr(base, 'Versioning', None)
                if options:
                    return options

        def get_version_default(versioning, name):
            return getattr(versioning, name,
                                getattr(get_versioning_defaults(), name))

        if attrs.has_key('Versioning'):
            versioning = attrs['Versioning']
        else:
            versioning = get_versioning_defaults()

        unique_together_with_fields = \
                                    get_version_default(versioning,
                                            'unique_together_with_fields')

        def is_model_field(field_name):
            '''
            Serch field in bases
            '''
            try:
                if isinstance(attrs[field_name], models.Field):
                    return True
            except KeyError:
                for base in bases:
                    meta = getattr(base, '_meta', None)
                    if meta:
                        fields_names = [f.name for f in meta.local_fields]
                        if field_name in fields_names:
                            return True
                return False
            else:
                return False

        def get_primary_key_field():
            '''
            Looking for a field that is a primary key.
            
            return <field name>
            '''
            for a_name, a in attrs.items():
                if getattr(a, 'primary_key', False):
                    return a_name
            for base in bases:
                meta = getattr(base, '_meta', None)
                if meta:
                    for a in meta.local_fields:
                        if getattr(a, 'primary_key', False):
                            return a.name
            return 'id'

        # Field Validation unique_together_with_fields
        if not (unique_together_with_fields and
            type(unique_together_with_fields) in (list, tuple) and
            len(unique_together_with_fields) > 0 and
            [True for i in unique_together_with_fields
                            if not type(i) in [list, tuple]] == []):
            raise VersionException('Incorrect field value '
                                   'unique_together_with_fields')
        else:
            # Replace all strings 'pk' the name of an existing field.
            utwf = list(unique_together_with_fields)
            for ug_i in range(len(utwf)):
                ug = list(utwf[ug_i])
                for field_name_i in range(len(ug)):
                    if ug[field_name_i] == 'pk':
                        ug[field_name_i] = get_primary_key_field()
                utwf[ug_i] = tuple(ug)
            unique_together_with_fields = tuple(utwf)

        # Field Validation fields_outside_changes
        fields_outside_changes_names = \
                        get_version_default(versioning,
                                            'fields_outside_changes')
        for field_name in fields_outside_changes_names:
            if not is_model_field(field_name):
                raise VersionException('The field [%s] does not inherit the '
                                   'django.db.models.Field' % (field_name,))

        # Field Validation hash_len
        hash_len = get_version_default(versioning, 'hash_len')
        if not (hash_len >= 64 and hash_len <= 512):
            raise VersionException('Hash_len field should be worth '
                                   'in the range of <64, 512>')

        # ####################################################
        # Get Meta fields
        # ####################################################
        if attrs.has_key('Meta'):
            meta = attrs['Meta']
            unique_together = getattr(meta, 'unique_together', ())
            if unique_together and not type(unique_together[0]) in (tuple, list):
                unique_together = (unique_together,)
        else:
            unique_together = ()

        # #####################################################
        # Add to unique_together, additional fields taken 
        # from Versioning.unique_together_with_fields
        # #####################################################

        # We are looking for whether a field is unique
        original_fields_names = [] # remember list real fields
        for field_name, field in attrs.items():
            if isinstance(field, models.Field):
                if getattr(field, 'primary_key', False):
                    continue
                unique = getattr(field, 'unique', False)
                if unique:
                    setattr(field, '_unique', False)
                    unique_together += ((field_name,),)
                original_fields_names.append(field_name)

        # add additional unique fields
        new_unique_together = ()
        for ut in unique_together:
            for utwf in unique_together_with_fields:
                new_unique_together += \
                        (tuple(ut) + \
                        tuple(utwf),)

        # set hash_len
        if hash_len <= 512:
            for base in bases:
                meta = getattr(base, '_meta', None)
                if meta:
                    for field in meta.local_fields:
                        if field.name == 'version_hash':
                            field.max_length = hash_len


        # set new data
        if attrs.has_key('Meta'):
            setattr(attrs['Meta'], 'unique_together', new_unique_together)
        else:
            class Meta:
                unique_together = new_unique_together
            attrs['Meta'] = Meta

        class VersioningNew: pass
        VersioningNew.unique_together_with_fields = unique_together_with_fields
        VersioningNew.fields_outside_changes = fields_outside_changes_names
        VersioningNew.hash_len = hash_len
        VersioningNew.original_fields_names = original_fields_names
        VersioningNew.original_primary_key = get_primary_key_field()
        attrs['Versioning'] = VersioningNew

        return super(VersionModelBase, cls).__new__(cls, name, bases, attrs)


class VersionModel(models.Model):
    '''
    
    class Version:

        # Foreign key for the visible parent object
        # default column name: 'version_parent_pk'
        field_name_parent_pk = 'version_parent_pk' 

        # Foreign key for the parent version object
        # default column name: 'version_parent_ver_pk'
        field_name_parent_version_pk = 'version_parent_ver_pk' 

        # Boolean field, Are there any child versions.
        # default column name: 'version_have_children'
        field_name_have_children = 'version_have_children'

        # Creation date of the current version
        # default column name: 'version_date'
        field_name_date = 'version_date' 
        
        # Current version hash
        # default column name: 'version_hash'
        field_name_hash = 'version_hash'  

        # Dictionary, where the key is the name of the field, and the 
        # value is the default value when you create a new version 
        # The following fields are not included to generate a hash.
        # Where the <variable> can take the following values​​:
        # - repchan.models.Value (Base Class)
        # - repchan.models.ValueDefault
        # - repchan.models.ValueParent
        # - repchan.models.ValueParentVersion
        # - default value
        # default: {}
        fields_outside_changes = {'notes':<variable>, ...}

    '''
    __metaclass__ = VersionModelBase

    VA_CLONE = 1 # Version action = clone


    version_parent_pk = models.ForeignKey(
                              'self',
                              blank=True,
                              null=True,
                              limit_choices_to={'version_parent_pk': None },
                              related_name='%(app_label)s_%(class)s_parentpk',
                              verbose_name=_(u'Visible parent object'))

    version_parent_rev_pk = models.ForeignKey(
                              'self',
                              blank=True,
                              null=True,
                              related_name='%(app_label)s_%(class)s_parentverpk',
                              verbose_name=_(u'Parent version object'))

    version_have_children = models.BooleanField(
                                default=False,
                                editable=False,
                                verbose_name=_(u'Whether the object'
                                                'has children'))

    version_date = models.DateTimeField(
                                  blank=True,
                                  null=True,
                                  auto_now_add=True,
                                  editable=False,
                                  verbose_name=_(u'Creation date'))

    version_hash = models.CharField(
                                    max_length=512,
                                    blank=True,
                                    default='',
                                    editable=False,
                                    verbose_name=_(u'Hash'))

    version_unique_on = models.NullBooleanField(
                               blank=True,
                               default=False,
                               verbose_name=_(u'Turn on the unique keys for revisions [True], '
                                               'turn on the unique keys for main [False], '
                                               'turn off the unique keys[None]'))

    version_in_trash = models.BooleanField(
                                       default=False,
                                       verbose_name=_(u'Is it in the trash'))


    objects = DefaultManager()
    objects_version = VersionManager()
    objects_raw = RawManager()

    def get_revisions(self, from_date=None, to_date=None, hash=None,
                                    head=None):
        '''
        Return list all versions for this property.
        '''
        if self.check_is_revision():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "revision".')

        if self.check_is_revision_new():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "revision new".')

        return self.__class__.objects_version.get_all_revisions_for(self)

    def get_revisions_tree(self):
        '''
        Return tree versions for the current object.
        Data structure:
        revisions = {<revision_root>: {<sub_revision_xi>:{None|<sub_revision_yi>} }}
        '''
        raise NotImplementedError('get_revisions_tree')

    def get_prev_revision(self):
        '''
        Return previous revision.
        '''
        if self.check_is_main_version():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "main".')

        return self.version_parent_rev_pk

    def get_next_revisions(self):
        '''
        Return list next revisions.
        '''
        if self.check_is_main_version():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "main".')

        if self.check_is_revision_new():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "revision new".')

        return self.__class__.objects_version.get_next_revisions(self)

    def set_as_main_version(self):
        '''
        Set the current reversion as the main version.
        
        If you try to re-set the major version as the main, 
        it is an exception thrown VersionException
        '''
        # Check if this is the main version
        if self.check_is_main_version():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "main".')

        if self.check_is_revision_new():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "revision new".')

        main_version = self.version_parent_pk

        # copy fields
        self._copy_fields(main_version)

        # copy mtm
        self._copy_changed_fields_mtm(main_version)

        # set outsidechanges 
        main_version = self._set_fields_outside_changes(
                                    main_version,
                                    'data_from_revision_to_main')

        # set versioning options
        main_version.version_parent_pk = None
        main_version.version_parent_rev_pk = self
        main_version.version_have_children = False
        main_version.version_date = NULL_DATE
        main_version.version_hash = ''
        main_version.version_unique_on = False
        main_version._save()

        revision_set_as_main.send(sender=self.__class__, instance=self)

    def check_is_main_version(self):
        '''
        Check if this is the main version.
        '''
        return self.version_parent_pk == None and \
                self.version_unique_on == False

    def check_is_revision(self):
        '''
        Check if this is the revision.
        '''
        return self.version_parent_pk != None and \
                self.version_unique_on == True

    def check_is_revision_new(self):
        '''
        Check if this is the revision new.
        '''
        return self.version_parent_pk != None and \
                self.version_unique_on == None

    def get_version_hash(self):
        '''
        Generated hash of the current object.
        '''
        keys = sorted(self._get_fieds_without_outside_changes())
        data = '=='.join([str(getattr(self, k)) for k in keys])
        return hashlib.sha512(data).hexdigest()[:self.Versioning.hash_len]

    def restore_from_trash(self):
        '''
        Restore from trash
        '''
        if self.version_in_trash:
            self.version_in_trash = False
            self._save()

    def delete(self, hard=False, using=None, *args, **kwargs):
        if self.check_is_revision():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "revision".')

        if self.check_is_revision_new():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "revision new".')

        # removed from the database or move to trash
        if self.version_in_trash or hard:
            # without sending signals post_delete, pre_delete
            self._delete(using=None, *args, **kwargs)
        elif hard:
            # with sending signals
            signal_allow(self, models.signals.pre_delete)
            signal_allow(self, models.signals.post_delete)

            self._delete(using=None, *args, **kwargs)

            signal_allow(self, models.signals.pre_delete, count=0)
            signal_allow(self, models.signals.post_delete, count=0)
        else:
            # with sending "virtual" signals
            using = using or router.db_for_write(self.__class__, instance=self)
            assert self._get_pk_val() is not None, \
                    "%s object can't be deleted because its %s attribute is set to None." % \
                    (self._meta.object_name, self._meta.pk.attname)

            collector = Collector(using=using)
            collector.collect([self])

            # send pre_delete signals
            for model, obj in collector.instances_with_model():
                if not model._meta.auto_created:
                    models.signals.pre_delete.send(
                        sender=model, instance=obj, using=using
                    )

            self.version_in_trash = True
            self._save()

            # send post_delete signals
            for model, obj in collector.instances_with_model():
                if not model._meta.auto_created:
                    models.signals.post_delete.send(
                        sender=model, instance=obj, using=using
                    )

    def _delete(self, using=None, *args, **kwargs):
        signal_send_off(self, models.signals.pre_delete)
        signal_send_off(self, models.signals.post_delete)

        super(VersionModel, self).delete(using=None, *args, **kwargs)

        signal_send_on(self, models.signals.pre_delete)
        signal_send_on(self, models.signals.post_delete)


    def _get_fieds_without_outside_changes(self):
        keys_original = self._get_fields_original_fields_names()
        keys_outside = self._get_fields_outside_changes().keys()
        keys = list(set(keys_original) - set(keys_outside))
        return keys

    def _get_fields_original_fields_names(self):
        return self.Versioning.original_fields_names

    def _get_fields_outside_changes(self):
        return getattr(self.__class__.Versioning, 'fields_outside_changes')

    def _get_fields_many_to_many(self):
        return [f.attname for f in self._meta.many_to_many]

    def _get_field_primary_key(self):
        return getattr(self.__class__.Versioning, 'original_primary_key')

    def _copy_fields(self, object_new):
        fields_names = list(
                            set(self._get_fieds_without_outside_changes()) -
                            set(self._get_fields_many_to_many()))
        for field_name in fields_names:
            setattr(object_new, field_name, getattr(self, field_name))
        return object_new

    def _copy_fields_mtm(self, object_new):
        fields_names = list(
                            set(self._get_fields_many_to_many()) -
                            set(self._get_fields_outside_changes().keys()))
        for field_mtm in fields_names:
            source = getattr(self, field_mtm.attname)
            destination = getattr(object_new, field.attname)
            for item in source.all():
                destination.add(item)
        return object_new

    def _copy_changed_fields_mtm(self, object_new):
        fields_names = list(
                            set(self._get_fields_many_to_many()) -
                            set(self._get_fields_outside_changes().keys()))

        for field_mtm in fields_names:
            source = getattr(self, field_mtm.attname)
            destination = getattr(object_new, field.attname)

            try:
                source_pk = zip(*source.all().values_list('pk'))[0]
            except IndexError:
                source_pk = []
            try:
                destination_pk = zip(*destination.all().values_list('pk'))[0]
            except IndexError:
                destination_pk = []

            # remove unnecessary fields
            intersection_pk = [i for i in source_pk if i in destination_pk]
            to_delete_pk = list(set(destination_pk) - set(intersection_pk))
            to_delete = destination.filter(pk__in=to_delete_pk)
            for td in to_delete:
                destination.remove(td)

            # copy additional fields
            for item in source.all():
                destination.add(item)
        return object_new

    def _set_fields_outside_changes(self, object_new, action):
        '''
        The method sets the attribute values ​​that are excluded 
        from versioning.
        
        action - action name derived from the class Value
        '''
        fields_outside = self._get_fields_outside_changes().items()
        # set fields outside changes
        for field_name, field_value in fields_outside:
            # check to see if it is a parser
            if isinstance(field_value, Value):
                setattr(object_new, field_name,
                        getattr(field_value, action)(self, object_new,
                                                     field_name))
            # otherwise, it is the default value
            else:
                setattr(object_new, field_name, field_value)
        return object_new

    def __setattr__(self, name, value):
        '''
        The implementation of access control attributes.
        
        [context - acces rights]
        main - Read/Write
        revision - Read
        revision - Read/Write
        '''
        fields = self._get_fields_original_fields_names()
        if (name in fields) and self.check_is_revision():
            if not "django/db/" in inspect.stack()[1][1]:
                raise VersionReadOnlyException('Varible "%s.%s" is read only' %
                                               (self.__class__.__name__,
                                                name,))
        super(VersionModel, self).__setattr__(name, value)

    def __delattr__(self, name):
        '''
        The implementation of access control attributes.
        
        [context - acces rights]
        main - Read/Write
        revision - Read
        revision - Read/Write
        '''
        fields = self._get_fields_original_fields_names()
        if (name in fields) and self.check_is_revision():
            if not "django/db/" in inspect.stack()[1][1]:
                raise VersionReadOnlyException('Varible "%s.%s" is read only' %
                                               (self.__class__.__name__,
                                                name,))
        super(VersionModel, self).__delattr__(name)

    def create_revision(self, using=None):
        '''
        Creates next revision of the current object.
        
        Cloning fields, taking into account the conditions in 
        Versioning.fields_outside_changes
        
        Keeps foreign keys and many to many relationships.
        '''
        if self.check_is_revision_new():
            raise VersionRevisionCreateException(
                                         'You can create a new revision from '
                                         'the object of type only '
                                         '"main" or "revision".')

        new_revision = self.__class__()

        new_revision = self._copy_fields(new_revision)

        # set version fields
        if self.check_is_main_version():
            new_revision.version_parent_pk = self
            new_revision.version_parent_rev_pk = self.version_parent_rev_pk
            new_revision.version_have_children = False
            new_revision.version_date = None
            #new_revision.version_hash = ''
        else:
            new_revision.version_parent_pk = self.version_parent_pk
            new_revision.version_parent_rev_pk = self
            new_revision.version_have_children = False
            new_revision.version_date = None
            #new_revision.version_hash = ''

        # Turn off unique keys
        new_revision.version_unique_on = None

        new_revision._save()

        new_revision = self._copy_fields_mtm(new_revision)

        if self.check_is_main_version():
            new_revision = self._set_fields_outside_changes(
                                        new_revision,
                                        'data_from_main_to_revision')
        else:
            new_revision = self._set_fields_outside_changes(
                                        new_revision,
                                        'data_from_revision_to_revision')

        new_revision._save()

        using = using or router.db_for_write(self.__class__, instance=self)
        revision_post_create.send(sender=self.__class__, instance=self,
                                  using=using)

        return new_revision

    def commit(self, using=None):
        '''
        Commit new revision
        '''
        if self.check_is_main_version() or self.check_is_revision():
            raise VersionDisabledMethodException('You can\'t commit this object.')

        # Check if there are changes
        hash = self.get_version_hash()
        old_hash = getattr(self.version_parent_rev_pk, 'version_hash', None)

        if old_hash != None and hash == old_hash:
            raise VersionCommitException('Nothing changed')

        self.version_hash = hash
        self.version_unique_on = True
        self._save()

        rev_old = self.version_parent_rev_pk
        if rev_old:
            rev_old.version_have_children = True
            rev_old._save()

        using = using or router.db_for_write(self.__class__, instance=self)
        revision_post_commit.send(sender=self.__class__, instance=self,
                                  using=using)

    def save(self, force_insert=False, force_update=False, using=None):
        # Check if this is the main version
        if self.check_is_revision():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "revision".')

        if self.check_is_revision_new():
            raise VersionDisabledMethodException(
                                  'The method can not be started from '
                                  'the object of type "revision new".')


        signal_allow(self, models.signals.pre_save)
        signal_allow(self, models.signals.post_save)

        self._save(force_insert=False, force_update=False, using=None)

        signal_allow(self, models.signals.pre_save, count=0)
        signal_allow(self, models.signals.post_save, count=0)

        #print dir(self)
        new_revision = self.create_revision()
        #print dir(new_revision)
        new_revision.commit()
        new_revision.set_as_main_version()


    def _save(self, *args, **kwargs):
        signal_send_off(self, models.signals.pre_save)
        signal_send_off(self, models.signals.post_save)

        super(VersionModel, self).save(*args, **kwargs)

        signal_send_on(self, models.signals.pre_save)
        signal_send_on(self, models.signals.post_save)

    class Meta:
        abstract = True

    class Versioning:
        # ('pk','version_suspended') - Used for objects just created. 
        #      Version_suspended field has a value of "null" for other objects,
        #      and deactivate this extra pair of unique keys.
        # ('version_hash',) - additional standard unique field
        unique_together_with_fields = (('version_hash', 'version_unique_on'),)
        fields_outside_changes = {}
        hash_len = 256 # hash length from 64 to 512
        # original_fields_names - auto generate
        # original_primary_key - auto generate

