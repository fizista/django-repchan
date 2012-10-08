=====
About
=====

Library for versioning of data from django models.

Conceptual design for the library:
- Easy implementation to the current models
- Must work with South migrations
- Transparent in action for the the standard features of the Django framework
- The logical structure of the database must be unaffected

Other similar projects:
- django-simple-history [`source <https://bitbucket.org/q/django-simple-history/src>`_]
- django-reversion [`source <https://github.com/etianen/django-reversion.git>`_]
- django-revisions [`source <https://github.com/stdbrouw/django-revisions>_`, `docs <http://stdbrouw.github.com/django-revisions/>_`]


django-repchan
==============

Truth table, access to the attributes of the context. 
+============+==========+==============+
| main       | revision | revision new |
+============+==========+==============+
| Read/Write | Read     | Read/Write   |
+------------+----------+--------------+
 If you try to write to a variable when it is a 'read only', 
 an exception is thrown VersionReadOnlyException.


Truth table attributes in the context.
+=======================+===============+====================+====================+
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
+=====================+=========================+=========================+==============================+
| self                | main                    | rev                     | rev new                      |
+=====================+=========================+=========================+==============================+
| create_revision     | copy self to rev new    | copy self to rev new    | raise  VersionRevision\      |
|                     |                         |                         | CreateException              |
+---------------------+-------------------------+-------------------------+------------------------------+
| commit              | raise VersionDisabled\  | raise  VersionDisabled\ | if self.hash != pre_rev.hash |
|                     | MethodException         | MethodException         | _save                        |
|                     |                         |                         | else VersionCommitException  |
+---------------------+-------------------------+-------------------------+------------------------------+
| set_as_main_version | raise VersionDisabled\  | copy self to main       | raise  VersionSetAs\         |
|                     | MethodException         |                         | MainException                |
+---------------------+-------------------------+-------------------------+------------------------------+
| save                | create_revision rev     | raise VersionDisabled\  | raise VersionDisabled\       |
|                     | commit rev              | MethodException         | MethodException              |
|                     | set_as_main_version rev |                         |                              |
+---------------------+-------------------------+-------------------------+------------------------------+
| delete              | object move to trash    | raise VersionDisabled\  | raise VersionDisabled\       |
|                     | if object in trash      | MethodException         | MethodException              |
|                     | then remove object      |                         |                              |
+---------------------+-------------------------+-------------------------+------------------------------+
|                     |                         |                         |                              |
+---------------------+-------------------------+-------------------------+------------------------------+
|                     |                         |                         |                              |
+---------------------+-------------------------+-------------------------+------------------------------+
|                     |                         |                         |                              |
+---------------------+-------------------------+-------------------------+------------------------------+

