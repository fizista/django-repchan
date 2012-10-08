# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Page', fields ['book', 'page_number', 'version_date', 'version_hash']
        db.delete_unique('repchantest_page', ['book_id', 'page_number', 'version_date', 'version_hash'])

        # Adding field 'Notebook.version_suspended'
        db.add_column('repchantest_notebook', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Notebook', fields ['note', 'version_suspended', 'number', 'id']
        db.create_unique('repchantest_notebook', ['note', 'version_suspended', 'number', 'id'])

        # Adding field 'Section.version_suspended'
        db.add_column('repchantest_section', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'AuthorAlias.version_suspended'
        db.add_column('repchantest_authoralias', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'AuthorAlias', fields ['version_suspended', 'name', 'id']
        db.create_unique('repchantest_authoralias', ['version_suspended', 'name', 'id'])

        # Adding field 'Page.version_suspended'
        db.add_column('repchantest_page', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Page', fields ['book', 'page_number', 'version_hash']
        db.create_unique('repchantest_page', ['book_id', 'page_number', 'version_hash'])

        # Adding unique constraint on 'Page', fields ['book', 'page_number', 'id', 'version_suspended']
        db.create_unique('repchantest_page', ['book_id', 'page_number', 'id', 'version_suspended'])

        # Adding field 'Book.version_suspended'
        db.add_column('repchantest_book', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CollectionNotebooks.version_suspended'
        db.add_column('repchantest_collectionnotebooks', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['book', 'page_number', 'id', 'version_suspended']
        db.delete_unique('repchantest_page', ['book_id', 'page_number', 'id', 'version_suspended'])

        # Removing unique constraint on 'Page', fields ['book', 'page_number', 'version_hash']
        db.delete_unique('repchantest_page', ['book_id', 'page_number', 'version_hash'])

        # Removing unique constraint on 'AuthorAlias', fields ['version_suspended', 'name', 'id']
        db.delete_unique('repchantest_authoralias', ['version_suspended', 'name', 'id'])

        # Removing unique constraint on 'Notebook', fields ['note', 'version_suspended', 'number', 'id']
        db.delete_unique('repchantest_notebook', ['note', 'version_suspended', 'number', 'id'])

        # Deleting field 'Notebook.version_suspended'
        db.delete_column('repchantest_notebook', 'version_suspended')

        # Deleting field 'Section.version_suspended'
        db.delete_column('repchantest_section', 'version_suspended')

        # Deleting field 'AuthorAlias.version_suspended'
        db.delete_column('repchantest_authoralias', 'version_suspended')

        # Deleting field 'Page.version_suspended'
        db.delete_column('repchantest_page', 'version_suspended')

        # Adding unique constraint on 'Page', fields ['book', 'page_number', 'version_date', 'version_hash']
        db.create_unique('repchantest_page', ['book_id', 'page_number', 'version_date', 'version_hash'])

        # Deleting field 'Book.version_suspended'
        db.delete_column('repchantest_book', 'version_suspended')

        # Deleting field 'CollectionNotebooks.version_suspended'
        db.delete_column('repchantest_collectionnotebooks', 'version_suspended')


    models = {
        'repchantest.author': {
            'Meta': {'unique_together': "(('name', 'surname'),)", 'object_name': 'Author'},
            'author_alias': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.AuthorAlias']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'repchantest.authoralias': {
            'Meta': {'unique_together': "(('name', 'version_hash'), ('name', 'id', 'version_suspended'))", 'object_name': 'AuthorAlias'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentverpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"}),
            'version_suspended': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.book': {
            'Meta': {'unique_together': '()', 'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_book_parentpk'", 'null': 'True', 'to': "orm['repchantest.Book']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_book_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Book']"}),
            'version_suspended': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.chapter': {
            'Meta': {'object_name': 'Chapter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'repchantest.collectionnotebooks': {
            'Meta': {'unique_together': '()', 'object_name': 'CollectionNotebooks'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notebooks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['repchantest.Notebook']", 'symmetrical': 'False'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_collectionnotebooks_parentpk'", 'null': 'True', 'to': "orm['repchantest.CollectionNotebooks']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_collectionnotebooks_parentverpk'", 'null': 'True', 'to': "orm['repchantest.CollectionNotebooks']"}),
            'version_suspended': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.notebook': {
            'Meta': {'unique_together': "(('note', 'number', 'version_hash'), ('note', 'number', 'id', 'version_suspended'))", 'object_name': 'Notebook'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_notebook_parentpk'", 'null': 'True', 'to': "orm['repchantest.Notebook']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_notebook_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Notebook']"}),
            'version_suspended': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.page': {
            'Meta': {'unique_together': "(('book', 'page_number', 'version_hash'), ('book', 'page_number', 'id', 'version_suspended'))", 'object_name': 'Page'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Book']"}),
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Chapter']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'page_number': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Section']"}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_page_parentpk'", 'null': 'True', 'to': "orm['repchantest.Page']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_page_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Page']"}),
            'version_suspended': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.section': {
            'Meta': {'unique_together': '()', 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_section_parentpk'", 'null': 'True', 'to': "orm['repchantest.Section']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_section_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Section']"}),
            'version_suspended': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['repchantest']