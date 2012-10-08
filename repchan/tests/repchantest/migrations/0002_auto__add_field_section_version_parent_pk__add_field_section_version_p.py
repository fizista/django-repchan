# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Section.version_parent_pk'
        db.add_column('repchantest_section', 'version_parent_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_section_parentpk', null=True, to=orm['repchantest.Section']),
                      keep_default=False)

        # Adding field 'Section.version_parent_rev_pk'
        db.add_column('repchantest_section', 'version_parent_rev_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_section_parentverpk', null=True, to=orm['repchantest.Section']),
                      keep_default=False)

        # Adding field 'Section.version_have_children'
        db.add_column('repchantest_section', 'version_have_children',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Section.version_date'
        db.add_column('repchantest_section', 'version_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Section.version_hash'
        db.add_column('repchantest_section', 'version_hash',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Section.version_in_trash'
        db.add_column('repchantest_section', 'version_in_trash',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AuthorAlias.version_parent_pk'
        db.add_column('repchantest_authoralias', 'version_parent_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_authoralias_parentpk', null=True, to=orm['repchantest.AuthorAlias']),
                      keep_default=False)

        # Adding field 'AuthorAlias.version_parent_rev_pk'
        db.add_column('repchantest_authoralias', 'version_parent_rev_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_authoralias_parentverpk', null=True, to=orm['repchantest.AuthorAlias']),
                      keep_default=False)

        # Adding field 'AuthorAlias.version_have_children'
        db.add_column('repchantest_authoralias', 'version_have_children',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'AuthorAlias.version_date'
        db.add_column('repchantest_authoralias', 'version_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AuthorAlias.version_hash'
        db.add_column('repchantest_authoralias', 'version_hash',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AuthorAlias.version_in_trash'
        db.add_column('repchantest_authoralias', 'version_in_trash',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Page.version_parent_pk'
        db.add_column('repchantest_page', 'version_parent_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_page_parentpk', null=True, to=orm['repchantest.Page']),
                      keep_default=False)

        # Adding field 'Page.version_parent_rev_pk'
        db.add_column('repchantest_page', 'version_parent_rev_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_page_parentverpk', null=True, to=orm['repchantest.Page']),
                      keep_default=False)

        # Adding field 'Page.version_have_children'
        db.add_column('repchantest_page', 'version_have_children',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Page.version_date'
        db.add_column('repchantest_page', 'version_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.version_hash'
        db.add_column('repchantest_page', 'version_hash',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.version_in_trash'
        db.add_column('repchantest_page', 'version_in_trash',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Book.version_parent_pk'
        db.add_column('repchantest_book', 'version_parent_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_book_parentpk', null=True, to=orm['repchantest.Book']),
                      keep_default=False)

        # Adding field 'Book.version_parent_rev_pk'
        db.add_column('repchantest_book', 'version_parent_rev_pk',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_book_parentverpk', null=True, to=orm['repchantest.Book']),
                      keep_default=False)

        # Adding field 'Book.version_have_children'
        db.add_column('repchantest_book', 'version_have_children',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Book.version_date'
        db.add_column('repchantest_book', 'version_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Book.version_hash'
        db.add_column('repchantest_book', 'version_hash',
                      self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Book.version_in_trash'
        db.add_column('repchantest_book', 'version_in_trash',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Section.version_parent_pk'
        db.delete_column('repchantest_section', 'version_parent_pk_id')

        # Deleting field 'Section.version_parent_rev_pk'
        db.delete_column('repchantest_section', 'version_parent_rev_pk_id')

        # Deleting field 'Section.version_have_children'
        db.delete_column('repchantest_section', 'version_have_children')

        # Deleting field 'Section.version_date'
        db.delete_column('repchantest_section', 'version_date')

        # Deleting field 'Section.version_hash'
        db.delete_column('repchantest_section', 'version_hash')

        # Deleting field 'Section.version_in_trash'
        db.delete_column('repchantest_section', 'version_in_trash')

        # Deleting field 'AuthorAlias.version_parent_pk'
        db.delete_column('repchantest_authoralias', 'version_parent_pk_id')

        # Deleting field 'AuthorAlias.version_parent_rev_pk'
        db.delete_column('repchantest_authoralias', 'version_parent_rev_pk_id')

        # Deleting field 'AuthorAlias.version_have_children'
        db.delete_column('repchantest_authoralias', 'version_have_children')

        # Deleting field 'AuthorAlias.version_date'
        db.delete_column('repchantest_authoralias', 'version_date')

        # Deleting field 'AuthorAlias.version_hash'
        db.delete_column('repchantest_authoralias', 'version_hash')

        # Deleting field 'AuthorAlias.version_in_trash'
        db.delete_column('repchantest_authoralias', 'version_in_trash')

        # Deleting field 'Page.version_parent_pk'
        db.delete_column('repchantest_page', 'version_parent_pk_id')

        # Deleting field 'Page.version_parent_rev_pk'
        db.delete_column('repchantest_page', 'version_parent_rev_pk_id')

        # Deleting field 'Page.version_have_children'
        db.delete_column('repchantest_page', 'version_have_children')

        # Deleting field 'Page.version_date'
        db.delete_column('repchantest_page', 'version_date')

        # Deleting field 'Page.version_hash'
        db.delete_column('repchantest_page', 'version_hash')

        # Deleting field 'Page.version_in_trash'
        db.delete_column('repchantest_page', 'version_in_trash')

        # Deleting field 'Book.version_parent_pk'
        db.delete_column('repchantest_book', 'version_parent_pk_id')

        # Deleting field 'Book.version_parent_rev_pk'
        db.delete_column('repchantest_book', 'version_parent_rev_pk_id')

        # Deleting field 'Book.version_have_children'
        db.delete_column('repchantest_book', 'version_have_children')

        # Deleting field 'Book.version_date'
        db.delete_column('repchantest_book', 'version_date')

        # Deleting field 'Book.version_hash'
        db.delete_column('repchantest_book', 'version_hash')

        # Deleting field 'Book.version_in_trash'
        db.delete_column('repchantest_book', 'version_in_trash')


    models = {
        'repchantest.author': {
            'Meta': {'unique_together': "(('name', 'surname'),)", 'object_name': 'Author'},
            'author_alias': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.AuthorAlias']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'repchantest.authoralias': {
            'Meta': {'object_name': 'AuthorAlias'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentverpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"})
        },
        'repchantest.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_book_parentpk'", 'null': 'True', 'to': "orm['repchantest.Book']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_book_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Book']"})
        },
        'repchantest.chapter': {
            'Meta': {'object_name': 'Chapter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'repchantest.page': {
            'Meta': {'unique_together': "(('book', 'page_number'),)", 'object_name': 'Page'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Book']"}),
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Chapter']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'page_number': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Section']"}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_page_parentpk'", 'null': 'True', 'to': "orm['repchantest.Page']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_page_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Page']"})
        },
        'repchantest.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_section_parentpk'", 'null': 'True', 'to': "orm['repchantest.Section']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_section_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Section']"})
        }
    }

    complete_apps = ['repchantest']