# -*- encoding: utf-8
from django.db import models
from repchan.models import ValueStandard, VersionModel


class AuthorAlias(VersionModel): # RC
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return u'%s' % (self.name,)

class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=150)
    author_alias = models.ForeignKey(AuthorAlias, blank=True, null=True)

    def __unicode__(self):
        return u'%s, %s' % (self.name, self.surname)

    class Meta:
        unique_together = (('name', 'surname'),)

class Section(VersionModel): # RC
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return u'%s' % (self.name,)

class Chapter(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return u'%s' % (self.name,)

class Book(VersionModel): # RC
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    log = models.CharField(max_length=5, blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.author)

    class Versioning:
        hash_len = 64

class Page(VersionModel): # RC
    page_number = models.IntegerField()
    book = models.ForeignKey(Book)
    chapter = models.ForeignKey(Chapter)
    section = models.ForeignKey(Section)
    contents = models.TextField()
    notes = models.TextField()

    def __unicode__(self):
        return u'%s[%d]' % (self.book, self.page_number)

    class Meta:
        unique_together = (('book', 'page_number'),)

    class Versioning:
        hash_len = 512
        unique_together_with_fields = (('version_hash', 'version_date',
                                        'version_unique_on'),)
        fields_outside_changes = {'notes': ValueStandard}

class Notebook(VersionModel): # RC
    idp = models.AutoField(primary_key=True)
    note = models.CharField(max_length=150)
    number = models.IntegerField()
    alias = models.CharField(max_length=150, default='none')

    def __unicode__(self):
        return u'%s[%d]' % (self.note, self.number)

    class Meta:
        unique_together = ('note', 'number')

    class Versioning:
        hash_len = 100
        unique_together_with_fields = (('version_hash',
                                        'version_unique_on'),)

class CollectionNotebooks(VersionModel):
    notebooks = models.ManyToManyField(Notebook)
