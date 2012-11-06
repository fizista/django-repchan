====================
About django-repchan
====================

Django-repchan allows easy data versioning for the Django framework.

Conceptual design for the library:

* Easy implementation to the current models
* Must work with South migrations
* Transparent in action for the the standard features of the Django framework
* The logical structure of the database must be unaffected

Other similar projects:

* django-simple-history [`source <https://bitbucket.org/q/django-simple-history/src>`_]
* django-reversion [`source <https://github.com/etianen/django-reversion.git>`_]
* django-revisions [`source <https://github.com/stdbrouw/django-revisions>`_, `docs <http://stdbrouw.github.com/django-revisions/>`_]

============
Requirements
============

Your application must use the migration South_.

* Django_ >= 1.4
* South_ >= 7.6
* Postgres (now with MySQL and SQLite does not work)


============
Installation
============

Stable release
--------------

Not yet ready.

What works:

* Versioning of data from models using Postgres database

Development
-----------

The latest development version can be installed directly from GitHub:

pip install http://github.com/fizista/django-repchan.git

=====
Setup
=====

* Add repchan to your INSTALLED_APPS

::

   INSTALLED_APPS += ('repchan',)
  
* Make sure that the database models you want to versioned, have been initiated by South_ migration.  Otherwise, use the following example initialization migration:
  
::

   ./manage.py convert_to_south your_app
  
* In your django models replace "django.db.models.Model" to "repchan.models.VersionModel", for example:

::

   # before changes
   from django.db import models
   
   class Book(VersionModel):
      title = models.CharField(max_length=200)

::

   # after changes
   from repchan.models import VersionModel
   
   class Book(VersionModel):
      title = models.CharField(max_length=200)
      
* Synchronize database

::

   ./manage.py syncdb
   ./manage.py schemamigration your_app --auto
   ./manage.py migrate your_app
   
=====
Usage
=====

::

   class Notebook(VersionModel): 
       note = models.CharField(max_length=150)
       number = models.IntegerField()
       alias = models.CharField(max_length=150, default='none')
   
       def __unicode__(self):
           return u'%s[%d]' % (self.note, self.number)

       class Meta:
           unique_together = ('note', 'number')

   >>> n = Notebook(note='abc',number=1,alias='ABC')
   >>> n.get_revisions()
   []
   >>> n.save() # Automatically created the first revision
   >>> n.get_revisions()
   [<Notebook: abc[1]>]
   >>> n.note = 'abc rev1'
   >>> n.save()
   >>> n.get_revisions() 
   [<Notebook: abc rev1[1]>, <Notebook: abc[1]>]
   >>> n = n.get_revisions()[1].set_as_main_version()
   >>> n
   <Notebook: abc rev1[1]>
   >>> n = Notebook.objects.all()[0]
   >>> n
   <Notebook: abc rev1[1]>
   
=======
Testing
=======

* add 'repchan' and 'repchan.tests.repchantest' to your INSTALLED_APPS

::

   INSTALLED_APPS += ('repchan', 'repchan.tests.repchantest')
   
   
* model initialization

::
   ./manage.py syncdb
   ./manage.py migrate repchan.tests.repchantest
   
* test run

::
   ./manage.py test repchan
    
   
=================================================
Tables range of methods, depending on the context
=================================================

Working range methods in the model depends on the context. We have three contexts:

* "main" - The object is in the normal state, which is the main version. You could compare it to an object without an installed data versioning.
* "revision" - The next version of the data object in the repository.
* "revision new" - Working copy, awaiting acceptance of the changes.


Truth table, access to the attributes of the context. 

+------------+----------+--------------+
| main       | revision | revision new |
+============+==========+==============+
| Read/Write | Read     | Read/Write   |
+------------+----------+--------------+

 If you try to write to a variable when it is a 'read only', 
 an exception is thrown VersionReadOnlyException.


Truth table attributes in the context.

+-----------------------+---------------+--------------------+--------------------+
|                       | main          | rev                | rev new            |
+=======================+===============+====================+====================+
| version_parent_pk     | None          | pk main            | pk main            |
+-----------------------+---------------+--------------------+--------------------+
| version_parent_rev_pk | pk rev        | None or pk old_rev | None or pk old_rev |
+-----------------------+---------------+--------------------+--------------------+
| version_have_children | False         | True if has        | False              |
+-----------------------+---------------+--------------------+--------------------+
| version_date          | null date     | rev create         | rev create         |
+-----------------------+---------------+--------------------+--------------------+
| version_hash          | null string   | hash               | null string        |
+-----------------------+---------------+--------------------+--------------------+
| version_unique_on     | False         | True               | None               |
+-----------------------+---------------+--------------------+--------------------+
| version_in_trash      | True or False | True or False      | True or False      |
+-----------------------+---------------+--------------------+--------------------+


Truth table commands in context.

+----------------------+-------------------------+-------------------------+------------------------------+
| self                 | main                    | rev                     | rev new                      |
+======================+=========================+=========================+==============================+
| create_revision      | copy self to rev new    | copy self to rev new    | raise  VersionRevision\      |
|                      |                         |                         | CreateException              |
+----------------------+-------------------------+-------------------------+------------------------------+
| commit               | raise VersionDisabled\  | raise  VersionDisabled\ | if self.hash != pre_rev.hash |
|                      | MethodException         | MethodException         | _save                        |
|                      |                         |                         | else VersionCommitException  |
+----------------------+-------------------------+-------------------------+------------------------------+
| set_as_main_version  | raise VersionDisabled\  | copy self to main       | raise  VersionSetAs\         |
|                      | MethodException         |                         | MainException                |
+----------------------+-------------------------+-------------------------+------------------------------+
| save                 | if main != main_rev     |                         |                              |
|                      | create_revision rev     | raise VersionDisabled\  | raise VersionDisabled\       |
|                      | commit rev              | MethodException         | MethodException              |
|                      | set_as_main_version rev |                         |                              |
+----------------------+-------------------------+-------------------------+------------------------------+
| delete               | object move to trash    | raise VersionDisabled\  | raise VersionDisabled\       |
|                      | if object in trash      | MethodException         | MethodException              |
|                      | then remove object      |                         |                              |
+----------------------+-------------------------+-------------------------+------------------------------+
| django.db.model.\    | normal                  |                         |                              |
| signals.pre_save     |                         | disabled                | disabled                     |
+----------------------+-------------------------+-------------------------+------------------------------+
| django.db.model.\    | normal                  |                         |                              |
| signals.post_save    |                         | disabled                | disabled                     |
+----------------------+-------------------------+-------------------------+------------------------------+
| django.db.model.\    | normal                  |                         |                              |
| signals.pre_delete   | if object in trash      | disabled                | disabled                     |
|                      | disabled                |                         |                              |
+----------------------+-------------------------+-------------------------+------------------------------+
| django.db.model.\    | normal                  |                         |                              |
| signals.post_delete  | if object in trash      | disabled                | disabled                     |
|                      | disabled                |                         |                              |
+----------------------+-------------------------+-------------------------+------------------------------+
| get_revisions        | return list django      | raise VersionDisabled\  | raise VersionDisabled\       |
|                      | QuerySet revisions      | MethodException         | MethodException              |
+----------------------+-------------------------+-------------------------+------------------------------+
| get_revisions_tree   | return tree list all    | raise VersionDisabled\  | raise VersionDisabled\       |
|                      | revisions               | MethodException         | MethodException              |
+----------------------+-------------------------+-------------------------+------------------------------+
| get_prev_revision    | raise VersionDisabled\  | return prev revision    | return prev revision         |
|                      | MethodException         | or None                 | or None                      |
+----------------------+-------------------------+-------------------------+------------------------------+
| get_next_revisions   | raise VersionDisabled\  | return list revisions   | raise VersionDisabled\       |
|                      | MethodException         |                         | MethodException              |
+----------------------+-------------------------+-------------------------+------------------------------+
| get_current_revision | return main revision    | raise VersionDisabled\  | raise VersionDisabled\       |
|                      |                         | MethodException         | MethodException              |
+----------------------+-------------------------+-------------------------+------------------------------+
|                      |                         |                         |                              |
+----------------------+-------------------------+-------------------------+------------------------------+


.. _South: http://south.readthedocs.org/en/latest/index.html
.. _Django: https://www.djangoproject.com/
