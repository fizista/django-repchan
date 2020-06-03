# -*- encoding: utf-8
import datetime
import hashlib

from django.utils import timezone
from django.utils.timezone import utc
from django.test import TestCase
from django.test import TransactionTestCase
from django.db import transaction
from django.db import IntegrityError

from repchan.tests.utils import TestCaseVersion
from repchan.tests.repchantest.models import AuthorAlias, Author, Section, \
                                             Chapter, Page, Book, Notebook, \
                                             CollectionNotebooks

from repchan.exceptions import VersionCommitException, \
                           VersionReadOnlyException, \
                           VersionDisabledMethodException
from repchan.models import ValueStandard, \
                           NULL_DATE

def gen_hash(hash_len=64, **kwargs):
    if type(hash_len) is not int:
        raise Exception('hash_len must be an integer')
    keys = kwargs.keys()
    keys.sort()
    data = '=='.join([str(kwargs[k]) for k in keys])
    return hashlib.sha512(data).hexdigest()[:hash_len]


def ipp_gen(start=1):
    '''
    Counter generator
    ipp = ipp_gen().next # 
    ipp() # i++
    '''
    i = start
    while 1:
        yield i
        i += 1


class TestModelBase(TestCaseVersion):

    def notebook_data_generator(self, number):
        return {'note': 'note_test_%s' % (number,),
                     'number': number,
                     'alias':'alias_test_%s' % (number,)}

    def notebook_hash_generator(self, number):
        return gen_hash(100, **self.notebook_data_generator(number))

    def notebook_generator_main(self, number, pk_rev=None):
        note_data = self.notebook_data_generator(number)
        note = Notebook(**note_data)
        note.version_parent_pk = None
        note.version_parent_rev_pk = pk_rev
        note.version_have_children = False
        note.version_date = timezone.localtime(timezone.now())
        note.version_hash = ''
        note.version_unique_on = False
        note.version_in_trash = False
        note._save()
        return note

    def notebook_generator_rev(self, number, pk_main, pk_rev_old=None,
                               have_children=False):
        '''
        * number - a unique sequence number generated data
        '''
        note_data = self.notebook_data_generator(number)
        note = Notebook(**note_data)
        note.version_parent_pk = pk_main
        note.version_parent_rev_pk = pk_rev_old
        note.version_have_children = have_children
        note.version_date = timezone.localtime(timezone.now())
        note.version_hash = self.notebook_hash_generator(number)
        note.version_unique_on = True
        note.version_in_trash = False
        note._save()
        return note

    def notebook_generator_rev_new(self, number, pk_main, pk_rev_old=None):
        note_data = self.notebook_data_generator(number)
        note = Notebook(**note_data)
        note.version_parent_pk = pk_main
        note.version_parent_rev_pk = pk_rev_old
        note.version_have_children = False
        note.version_date = timezone.localtime(timezone.now())
        note.version_hash = ''
        note.version_unique_on = None
        note.version_in_trash = False
        note._save()
        return note

    def assertVersionStatus(
                        self, version_object,
                        version_parent_pk,
                        version_parent_rev_pk,
                        version_have_children,
                        version_hash,
                        version_unique_on,
                        version_in_trash,
                        version_date_pre=None,
                        version_date_post=None,
                        version_date=None,
                        version_counter=None,
                        info=''):
        def assertEqual(a, b, var_name=''):
            self.assertEqual(a, b, msg='%s, var_name=%s ["%s" != "%s"]' %
                            (info, var_name, a, b))
        def assertTrue(a, var_name):
            self.assertTrue(a, msg='%s %s. False is not true' %
                            (info, var_name))

        assertEqual(version_parent_pk,
                     version_object.version_parent_pk,
                     'version_parent_pk')
        assertEqual(version_parent_rev_pk,
                     version_object.version_parent_rev_pk,
                     'version_parent_rev_pk')
        assertEqual(version_have_children,
                     version_object.version_have_children,
                     'version_have_children')
        assertEqual(version_parent_pk,
                     version_object.version_parent_pk,
                     'version_parent_pk')
        if version_date_pre and version_date_post:
            self.assertTrue(version_date_pre < version_object.version_date and
                        version_date_post > version_object.version_date,
                        msg='"%s", var_name=version_date. '
                            'Outside the permitted time.\n'
                            'Excepted between [%s;%s]\n'
                            'The time received [%s]' %
                            (info,
                             version_date_pre,
                             version_date_post,
                             version_object.version_date))
        if version_date:
            self.assertTrue(version_date == version_object.version_date,
                        msg='%s, var_name=version_date. '
                            'The expected time is %s, '
                            'but the resulting time is %s' %
                            (info, version_date, version_object.version_date))
        assertEqual(version_hash,
                     version_object.version_hash,
                     'version_hash')
        assertEqual(version_unique_on,
                     version_object.version_unique_on,
                     'version_unique_on')
        assertEqual(version_in_trash,
                     version_object.version_in_trash,
                     'version_in_trash')
        if version_counter:
            assertEqual(version_counter,
                     version_object.version_counter,
                     'version_counter')

    def assertEqialModelObjectPk(self, first, second):
        '''
        Compare primary keys in objects.
        '''
        self.assertEqual(
                         list(first.order_by('pk').values_list('pk')),
                         list(second.order_by('pk').values_list('pk'))
                         )

    def time_start_stop(self, method, *args, **kwargs):
        '''
        return (start_date, end_date, output)
        '''
        start_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        output = method(*args, **kwargs)
        end_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        return (start_date, end_date, output)

    def time_now(self):
        '''
        return <datetime obj>
        '''
        return datetime.datetime.utcnow().replace(tzinfo=utc)


class TestModelVersions(TestModelBase):
    #fixtures = ['books', ]

    def setUp(self):
        Notebook.objects_raw.all().delete()
        super(TestModelVersions, self).setUp()

    def test_generators(self):
        note_main = self.notebook_generator_main(1)

        self.assertVersionStatus(note_main,
                        version_parent_pk=None,
                        version_parent_rev_pk=None,
                        version_have_children=False,
                        version_hash='',
                        version_unique_on=False,
                        version_in_trash=False,
                        info='main gen test')

        note_rev_new = self.notebook_generator_rev_new(2, note_main)

        self.assertVersionStatus(note_rev_new,
                        version_parent_pk=note_main,
                        version_parent_rev_pk=None,
                        version_have_children=False,
                        version_hash='',
                        version_unique_on=None,
                        version_in_trash=False,
                        info='rev new gen test')

        note_rev = self.notebook_generator_rev(3, note_main, note_rev_new, True)

        self.assertVersionStatus(note_rev,
                        version_parent_pk=note_main,
                        version_parent_rev_pk=note_rev_new,
                        version_have_children=True,
                        version_hash=self.notebook_hash_generator(3),
                        version_unique_on=True,
                        version_in_trash=False,
                        info='rev gen test')

    def test_save(self):
        note_data = self.notebook_data_generator(1)
        note_main = Notebook(**note_data)
        start_date, end_date, null = self.time_start_stop(note_main.save)

        note1_rev1 = Notebook.objects_raw.filter(note=note_main.note,
                                                 version_unique_on=True)[0]

        note_main = Notebook.objects.get(pk=note_main.pk)

        dg = self.notebook_data_generator(1)
        self.assertEqual([dg['note'], dg['number'], dg['alias']],
                         [note1_rev1.note, note1_rev1.number, note1_rev1.alias])
        self.assertEqual([note_main.note, note_main.number, note_main.alias],
                         [note1_rev1.note, note1_rev1.number, note1_rev1.alias])
        self.assertVersionStatus(note_main,
                        version_parent_pk=None,
                        version_parent_rev_pk=note1_rev1,
                        version_have_children=False,
                        version_date_pre=start_date,
                        version_date_post=end_date,
                        version_hash='',
                        version_unique_on=False,
                        version_in_trash=False,
                        version_counter=1,
                        info='main, copy rev1')

        with self.assertRaises(VersionDisabledMethodException):
            note1_rev1.save()

        note1_rev2_new = self.notebook_generator_rev_new(3, note_main)
        with self.assertRaises(VersionDisabledMethodException):
            note1_rev2_new.save()


    def test_commit(self):
        note_main = self.notebook_generator_main(1)
        note_rev1_new = self.notebook_generator_rev_new(1, note_main)
        date_rev_new = note_rev1_new.version_date

        # commit succes, first revision
        note_rev1_new.commit()

        self.assertVersionStatus(note_rev1_new,
                        version_parent_pk=note_main,
                        version_parent_rev_pk=None,
                        version_have_children=False,
                        version_date=date_rev_new,
                        version_hash=self.notebook_hash_generator(1),
                        version_unique_on=True,
                        version_in_trash=False,
                        info='first revision')

        note_rev2_new = self.notebook_generator_rev_new(2, note_main, note_rev1_new)
        # commit succes, second revision, change first rev, and now has
        note_rev2_new.commit()

        self.assertVersionStatus(note_rev1_new,
                        version_parent_pk=note_main,
                        version_parent_rev_pk=None,
                        version_have_children=True, # This has changed
                        version_date=date_rev_new,
                        version_hash=self.notebook_hash_generator(1),
                        version_unique_on=True,
                        version_in_trash=False,
                        info='first revision, has children')

        self.assertVersionStatus(note_rev2_new,
                        version_parent_pk=note_main,
                        version_parent_rev_pk=note_rev1_new,
                        version_have_children=False,
                        version_hash=self.notebook_hash_generator(2),
                        version_unique_on=True,
                        version_in_trash=False,
                        info='second revision')

        with self.assertRaises(VersionDisabledMethodException):
            note_main.commit()

        with self.assertRaises(VersionDisabledMethodException):
            note_rev2_new.commit()

    def test_check_is(self):
        note_main = self.notebook_generator_main(1)
        note_rev1_new = self.notebook_generator_rev_new(1, note_main)
        note_rev2 = self.notebook_generator_rev(2, note_main, None, True)

        self.assertTrue(note_main.check_is_main_version())
        self.assertFalse(note_main.check_is_revision())
        self.assertFalse(note_main.check_is_revision_new())

        self.assertFalse(note_rev1_new.check_is_main_version())
        self.assertFalse(note_rev1_new.check_is_revision())
        self.assertTrue(note_rev1_new.check_is_revision_new())

        self.assertFalse(note_rev2.check_is_main_version())
        self.assertTrue(note_rev2.check_is_revision())
        self.assertFalse(note_rev2.check_is_revision_new())

    def test_create_revision(self):
        note_main = self.notebook_generator_main(1)

        rev_new1 = note_main.create_revision()
        self.assertEqual([note_main.note, note_main.number, note_main.alias],
                         [rev_new1.note, rev_new1.number, rev_new1.alias])
        self.assertVersionStatus(rev_new1,
                        version_parent_pk=note_main,
                        version_parent_rev_pk=None,
                        version_have_children=False,
                        version_hash='',
                        version_unique_on=None,
                        version_in_trash=False,
                        info='first new revision')

        # Test copy of the object, not from the database.       
        note_main.note = 'somethin'
        rev_new2 = note_main.create_revision()
        self.assertEqual([note_main.note, note_main.number, note_main.alias],
                         [rev_new2.note, rev_new2.number, rev_new2.alias])
        self.assertVersionStatus(rev_new2,
                        version_parent_pk=note_main,
                        version_parent_rev_pk=None,
                        version_have_children=False,
                        version_hash='',
                        version_unique_on=None,
                        version_in_trash=False,
                        info='second new revision')


        # Test copy of the object, from another revision.
        rev_new1.commit()
        rev_new3 = rev_new1.create_revision()
        self.assertEqual([rev_new1.note, rev_new1.number, rev_new1.alias],
                         [rev_new3.note, rev_new3.number, rev_new3.alias])
        self.assertVersionStatus(rev_new3,
                        version_parent_pk=note_main,
                        version_parent_rev_pk=rev_new1,
                        version_have_children=False,
                        version_hash='',
                        version_unique_on=None,
                        version_in_trash=False,
                        info='3rd new revision')

        # It is forbidden to create the revision of the previous revision 
        # is not accepted.
        with self.assertRaises(VersionDisabledMethodException):
            rev_new2.create_revision()

    def test_set_as_main_version(self):
        note_main = self.notebook_generator_main(2)
        date_main = note_main.version_date
        note_rev2 = self.notebook_generator_rev(2, note_main, None, True)
        note_rev3 = self.notebook_generator_rev(3, note_main, note_rev2)
        note_main.version_parent_rev_pk = note_rev2
        note_main.version_date = note_rev2.version_date
        note_main._save()

        self.assertEqual([note_main.note, note_main.number, note_main.alias],
                         [note_rev2.note, note_rev2.number, note_rev2.alias])
        self.assertVersionStatus(note_main,
                        version_parent_pk=None,
                        version_parent_rev_pk=note_rev2,
                        version_have_children=False,
                        version_date=note_rev2.version_date,
                        version_hash='',
                        version_unique_on=False,
                        version_in_trash=False,
                        version_counter=0, # zero, because it is the object 
                                           # created for test
                        info='is it rev2')

        start_date, end_date, null = self.time_start_stop(
                                          note_rev3.set_as_main_version)

        self.assertEqual([note_main.note, note_main.number, note_main.alias],
                         [note_rev3.note, note_rev3.number, note_rev3.alias])
        self.assertVersionStatus(note_main,
                        version_parent_pk=None,
                        version_parent_rev_pk=note_rev3,
                        version_have_children=False,
                        version_date_pre=start_date,
                        version_date_post=end_date,
                        version_hash='',
                        version_unique_on=False,
                        version_in_trash=False,
                        version_counter=1,
                        info='is it rev3')

        note_main = self.notebook_generator_main(5)
        note_rev_new = self.notebook_generator_rev_new(6, note_main)

        with self.assertRaises(VersionDisabledMethodException):
            note_main.set_as_main_version()

        with self.assertRaises(VersionDisabledMethodException):
            note_rev_new.set_as_main_version()

    def test_delete(self):
        note_main = self.notebook_generator_main(2)
        date_main = note_main.version_date
        note_rev2 = self.notebook_generator_rev(2, note_main, None, True)
        note_rev3 = self.notebook_generator_rev_new(3, note_main, note_rev2)
        note_main.version_parent_rev_pk = note_rev2
        note_main.version_date = note_rev2.version_date
        note_main._save()

        note_main.delete()
        self.assertTrue(len(Notebook.objects.
                         filter(note=self.notebook_data_generator(2)['note']).
                                            values_list()) == 0)
        self.assertTrue(len(Notebook.objects.in_trash()) == 1)

        note_main.restore_from_trash()
        self.assertTrue(len(Notebook.objects.
                         filter(note=self.notebook_data_generator(2)['note']).
                                            values_list()) == 1)
        self.assertTrue(len(Notebook.objects.in_trash()) == 0)

        note_main.delete(hard=True)
        self.assertTrue(len(Notebook.objects.
                         filter(note=self.notebook_data_generator(2)['note']).
                                            values_list()) == 0)
        self.assertTrue(len(Notebook.objects.in_trash()) == 0)



        with self.assertRaises(VersionDisabledMethodException):
            note_rev2.delete()

        with self.assertRaises(VersionDisabledMethodException):
            note_rev3.delete()

    def test_context_attribute_access(self):
        # can write
        note_main = self.notebook_generator_main(2)
        note_main.note = 'new note data'
        note_main.number = 2
        note_main.alias = 'new alias data'

        note_rev_new = self.notebook_generator_rev(2, note_main)
        note_main.note = 'new note data'
        note_main.number = 2
        note_main.alias = 'new alias data'

        # can't write
        note_rev2 = self.notebook_generator_rev(3, note_main)
        with self.assertRaises(VersionReadOnlyException):
            note_rev2.note = 'new note data'
        with self.assertRaises(VersionReadOnlyException):
            note_rev2.number = 2
        with self.assertRaises(VersionReadOnlyException):
            note_rev2.alias = 'new alias data'

    def test_get_revisions(self):

        ipp = ipp_gen(1).next

        note_main = self.notebook_generator_main(ipp())

        note_rev1 = self.notebook_generator_rev(ipp(), note_main, None, True)
        note_rev1_1 = self.notebook_generator_rev(ipp(), note_main, note_rev1, True)
        note_rev1_1_1 = self.notebook_generator_rev_new(ipp(), note_main, note_rev1_1)

        note_rev1_2 = self.notebook_generator_rev(ipp(), note_main, note_rev1)


        note2_main = self.notebook_generator_main(ipp())

        note2_rev1 = self.notebook_generator_rev(ipp(), note2_main, None, True)
        note2_rev1_1 = self.notebook_generator_rev(ipp(), note2_main, note_rev1, True)
        note2_rev1_1_1 = self.notebook_generator_rev_new(ipp(), note2_main, note_rev1_1)

        note2_rev1_2 = self.notebook_generator_rev(ipp(), note2_main, note_rev1)

        # check to see if there are revisions from one object
        # 
        self.assertEqual(
                         list(note_main.get_revisions().order_by('pk').values_list('pk')),
                         [(note_rev1.pk,),
                          (note_rev1_1.pk,),
                          (note_rev1_2.pk,)])

    def test_get_prev_revision(self):

        ipp = ipp_gen(1).next

        note_main = self.notebook_generator_main(ipp())

        note_rev1 = self.notebook_generator_rev(ipp(), note_main, None, True)
        note_rev1_1 = self.notebook_generator_rev(ipp(), note_main, note_rev1, True)
        note_rev1_1_1 = self.notebook_generator_rev_new(ipp(), note_main, note_rev1_1)

        note_rev1_2 = self.notebook_generator_rev(ipp(), note_main, note_rev1)

        self.assertEqual(
                         (note_rev1_1_1.get_prev_revision().pk,
                          note_rev1_1.get_prev_revision().pk,
                          note_rev1.get_prev_revision(),
                          note_rev1_2.get_prev_revision().pk,),
                         (note_rev1_1.pk,
                          note_rev1.pk,
                          None,
                          note_rev1.pk))

    def test_get_next_revisions(self):

        ipp = ipp_gen(1).next

        note_main = self.notebook_generator_main(ipp())

        note_rev1 = self.notebook_generator_rev(ipp(), note_main, None, True)
        note_rev1_1 = self.notebook_generator_rev(ipp(), note_main, note_rev1, True)
        note_rev1_1_1 = self.notebook_generator_rev(ipp(), note_main, note_rev1_1)

        note_rev1_2 = self.notebook_generator_rev(ipp(), note_main, note_rev1)


        # no next revisions
        self.assertEqual(
                         list(note_rev1_1_1.get_next_revisions().\
                                order_by('pk').values_list('pk')),
                         []
                         )

        # one revision
        self.assertEqual(
                         list(note_rev1_1.get_next_revisions().\
                                order_by('pk').values_list('pk')),
                         [(note_rev1_1_1.pk,)]
                         )

        # two revision
        self.assertEqual(
                         list(note_rev1.get_next_revisions().\
                                order_by('pk').values_list('pk')),
                         [(note_rev1_1.pk,), (note_rev1_2.pk,)]
                         )


    def test_copy_mtm_fields(self):

        ipp = ipp_gen(1).next

        note1_main = self.notebook_generator_main(ipp())
        note2_main = self.notebook_generator_main(ipp())
        note3_main = self.notebook_generator_main(ipp())
        note4_main = self.notebook_generator_main(ipp())
        note5_main = self.notebook_generator_main(ipp())

        cn = CollectionNotebooks()
        cn._save()
        cn.notebooks.add(note1_main)
        cn.notebooks.add(note2_main)
        cn.notebooks.add(note3_main)
        cn._save()

        cn1 = CollectionNotebooks()
        cn1._save()

        cn1 = cn._copy_fields_mtm(cn1)
        cn1._save()

        self.assertEqialModelObjectPk(cn.notebooks.all(), cn1.notebooks.all())

        cn.notebooks.add(note4_main)
        cn.notebooks.add(note5_main)
        cn.notebooks.remove(note2_main, note1_main)
        cn._save()

        cn1 = cn._copy_changed_fields_mtm(cn1)
        cn1.save()

        self.assertEqialModelObjectPk(cn.notebooks.all(), cn1.notebooks.all())





class TestModelTransparency(TestCaseVersion):
    #fixtures = ['books', ]

    def setUp(self):
        Notebook.objects_raw.all().delete()
        super(TestModelTransparency, self).setUp()

    def tearDown(self):
        Notebook.objects_raw.all().delete()
        super(TestModelTransparency, self).setUp()

    def test_count_objects(self):

        # Create first
        note_data = {'note': 'asdfgh', 'number': 1, 'alias':'bb'}
        Notebook(**note_data).save()

        self.assertCountObject(1, Notebook)

        # Create second
        note_data['number'] = 2
        Notebook(**note_data).save()

        self.assertCountObject(2, Notebook)

        # Change first
        note = Notebook.objects.all()[0]
        note.alias = 'aa'
        note.save()

        self.assertCountObject(2, Notebook)

        # Remove second
        Notebook.objects.all()[1].delete()

        self.assertCountObject(1, Notebook)

    def test_trash(self):

        note_data = {'note': 'asdfgh', 'number': 31, 'alias':'bb'}
        note1 = Notebook(**note_data)
        note1.save()

        note_data['number'] = 33
        note2 = Notebook(**note_data)
        note2.save()

        # Trash is empty
        self.assertCountObjectInTrash(0, Notebook)
        self.assertCountObject(2, Notebook)

        note1.delete()
        # Trash something already has.
        self.assertCountObjectInTrash(1, Notebook)
        self.assertCountObject(1, Notebook)

        # Restore from trash
        note1_from_trash = Notebook.objects.in_trash()[0]
        note1_from_trash.restore_from_trash()

        # Trash now is empty
        self.assertCountObjectInTrash(0, Notebook)
        self.assertCountObject(2, Notebook)

        note1.delete(hard=True)
        self.assertCountObjectInTrash(0, Notebook)
        self.assertCountObject(1, Notebook)


class TestUnique(TransactionTestCase):
    fixtures = ['books.json', ]

    def setUp(self):
        super(TestUnique, self).setUp()

    def test_exists_unique(self):
        # Check whether an abstract class add additional fields unique.
        classes = {
                   AuthorAlias: (
                                 ('name', 'version_hash', 'version_unique_on'),
                                 ('id',)),
                   Section: (('id',),),
                   Book: (('id',),),
                   Page: (('book', 'page_number', 'version_hash',
                           'version_date', 'version_unique_on'),
                          ('id',)),
                   }

        for current_class, expected_response in classes.items():
            object = current_class.objects.all()[0]
            uniques = zip(*object._get_unique_checks()[0])[1]
            self.assertEqual(
                     uniques,
                     expected_response,
                     'For %s, the expected answer is %s, but it received %s.' %
                        (current_class, expected_response, uniques))

    def test_unique_field(self):
        # Check the model, which contains a field with the option unique = True
        AuthorAlias(name='unique 1').save()
        with self.assertRaises(IntegrityError):
            AuthorAlias(name='unique 1').save()
        transaction.rollback()

    def test_unique_together(self):

#        item = { 'page_number':10,
#                 'book':Book.objects_raw.get(pk=1),
#                 'chapter':Chapter.objects.get(pk=1),
#                 'section':Section.objects_raw.get(pk=1),
#                 'contents':'asdasd',
#                 'notes' : 'oooo' }
#
#        Page(**item).save()
#        with self.assertRaises(IntegrityError):
#            Page(**item).save()
#        transaction.rollback()

        note_data = {'note': 'qwerty', 'number': 1, 'alias':'aa'}
        Notebook(**note_data).save()
        with self.assertRaises(IntegrityError):
            Notebook(**note_data).save()
        transaction.rollback()


class TestValue(TestModelBase):

    def test_valuestandard(self):
        note_main = self.notebook_generator_main(1)
        note_rev = self.notebook_generator_rev(1, note_main, None, False)

        # Test ValueStandard
        vs = ValueStandard('new_value')
        self.assertEqual(
                         vs._get_default_model_value(note_main, 'alias'),
                         'none')
        self.assertEqual(
                         vs._get_default(note_main, 'alias'),
                         'new_value')
        self.assertEqual(
                         vs.data_from_main_to_revision(note_main, note_rev, 'alias'),
                         'new_value')
        self.assertEqual(
                         vs.data_from_revision_to_main(note_main, note_rev, 'alias'),
                         note_rev.alias)
        self.assertEqual(
                         vs.data_from_revision_to_revision(note_main, note_rev, 'alias'),
                         'new_value')


