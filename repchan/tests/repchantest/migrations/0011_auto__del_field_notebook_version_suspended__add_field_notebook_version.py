# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Page', fields ['book', 'page_number', 'id', 'version_suspended']
        db.delete_unique('repchantest_page', ['book_id', 'page_number', 'id', 'version_suspended'])

        # Removing unique constraint on 'Page', fields ['book', 'page_number', 'version_date', 'version_hash']
        db.delete_unique('repchantest_page', ['book_id', 'page_number', 'version_date', 'version_hash'])

        # Removing unique constraint on 'AuthorAlias', fields ['version_suspended', 'name', 'id']
        db.delete_unique('repchantest_authoralias', ['version_suspended', 'name', 'id'])

        # Removing unique constraint on 'AuthorAlias', fields ['version_hash', 'name']
        db.delete_unique('repchantest_authoralias', ['version_hash', 'name'])

        # Removing unique constraint on 'Notebook', fields ['note', 'version_suspended', 'number', 'idp']
        db.delete_unique('repchantest_notebook', ['note', 'version_suspended', 'number', 'idp'])

        # Removing unique constraint on 'Notebook', fields ['note', 'version_hash', 'number']
        db.delete_unique('repchantest_notebook', ['note', 'version_hash', 'number'])

        # Deleting field 'Notebook.version_suspended'
        db.delete_column('repchantest_notebook', 'version_suspended')

        # Adding field 'Notebook.version_unique_off'
        db.add_column('repchantest_notebook', 'version_unique_off',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Notebook.version_hash'
        db.alter_column('repchantest_notebook', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512))
        # Adding unique constraint on 'Notebook', fields ['note', 'version_hash', 'number', 'version_unique_off']
        db.create_unique('repchantest_notebook', ['note', 'version_hash', 'number', 'version_unique_off'])

        # Deleting field 'Section.version_suspended'
        db.delete_column('repchantest_section', 'version_suspended')

        # Adding field 'Section.version_unique_off'
        db.add_column('repchantest_section', 'version_unique_off',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Section.version_hash'
        db.alter_column('repchantest_section', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512))
        # Deleting field 'AuthorAlias.version_suspended'
        db.delete_column('repchantest_authoralias', 'version_suspended')

        # Adding field 'AuthorAlias.version_unique_off'
        db.add_column('repchantest_authoralias', 'version_unique_off',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'AuthorAlias.version_hash'
        db.alter_column('repchantest_authoralias', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512))
        # Adding unique constraint on 'AuthorAlias', fields ['version_hash', 'name', 'version_unique_off']
        db.create_unique('repchantest_authoralias', ['version_hash', 'name', 'version_unique_off'])

        # Deleting field 'Page.version_suspended'
        db.delete_column('repchantest_page', 'version_suspended')

        # Adding field 'Page.version_unique_off'
        db.add_column('repchantest_page', 'version_unique_off',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Page.version_hash'
        db.alter_column('repchantest_page', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512))
        # Adding unique constraint on 'Page', fields ['book', 'page_number', 'version_date', 'version_unique_off', 'version_hash']
        db.create_unique('repchantest_page', ['book_id', 'page_number', 'version_date', 'version_unique_off', 'version_hash'])

        # Deleting field 'Book.version_suspended'
        db.delete_column('repchantest_book', 'version_suspended')

        # Adding field 'Book.version_unique_off'
        db.add_column('repchantest_book', 'version_unique_off',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Book.version_hash'
        db.alter_column('repchantest_book', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512))
        # Deleting field 'CollectionNotebooks.version_suspended'
        db.delete_column('repchantest_collectionnotebooks', 'version_suspended')

        # Adding field 'CollectionNotebooks.version_unique_off'
        db.add_column('repchantest_collectionnotebooks', 'version_unique_off',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'CollectionNotebooks.version_hash'
        db.alter_column('repchantest_collectionnotebooks', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512))

    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['book', 'page_number', 'version_date', 'version_unique_off', 'version_hash']
        db.delete_unique('repchantest_page', ['book_id', 'page_number', 'version_date', 'version_unique_off', 'version_hash'])

        # Removing unique constraint on 'AuthorAlias', fields ['version_hash', 'name', 'version_unique_off']
        db.delete_unique('repchantest_authoralias', ['version_hash', 'name', 'version_unique_off'])

        # Removing unique constraint on 'Notebook', fields ['note', 'version_hash', 'number', 'version_unique_off']
        db.delete_unique('repchantest_notebook', ['note', 'version_hash', 'number', 'version_unique_off'])

        # Adding field 'Notebook.version_suspended'
        db.add_column('repchantest_notebook', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Notebook.version_unique_off'
        db.delete_column('repchantest_notebook', 'version_unique_off')


        # Changing field 'Notebook.version_hash'
        db.alter_column('repchantest_notebook', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Adding unique constraint on 'Notebook', fields ['note', 'version_hash', 'number']
        db.create_unique('repchantest_notebook', ['note', 'version_hash', 'number'])

        # Adding unique constraint on 'Notebook', fields ['note', 'version_suspended', 'number', 'idp']
        db.create_unique('repchantest_notebook', ['note', 'version_suspended', 'number', 'idp'])

        # Adding field 'Section.version_suspended'
        db.add_column('repchantest_section', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Section.version_unique_off'
        db.delete_column('repchantest_section', 'version_unique_off')


        # Changing field 'Section.version_hash'
        db.alter_column('repchantest_section', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Adding field 'AuthorAlias.version_suspended'
        db.add_column('repchantest_authoralias', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'AuthorAlias.version_unique_off'
        db.delete_column('repchantest_authoralias', 'version_unique_off')


        # Changing field 'AuthorAlias.version_hash'
        db.alter_column('repchantest_authoralias', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Adding unique constraint on 'AuthorAlias', fields ['version_hash', 'name']
        db.create_unique('repchantest_authoralias', ['version_hash', 'name'])

        # Adding unique constraint on 'AuthorAlias', fields ['version_suspended', 'name', 'id']
        db.create_unique('repchantest_authoralias', ['version_suspended', 'name', 'id'])

        # Adding field 'Page.version_suspended'
        db.add_column('repchantest_page', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Page.version_unique_off'
        db.delete_column('repchantest_page', 'version_unique_off')


        # Changing field 'Page.version_hash'
        db.alter_column('repchantest_page', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Adding unique constraint on 'Page', fields ['book', 'page_number', 'version_date', 'version_hash']
        db.create_unique('repchantest_page', ['book_id', 'page_number', 'version_date', 'version_hash'])

        # Adding unique constraint on 'Page', fields ['book', 'page_number', 'id', 'version_suspended']
        db.create_unique('repchantest_page', ['book_id', 'page_number', 'id', 'version_suspended'])

        # Adding field 'Book.version_suspended'
        db.add_column('repchantest_book', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Book.version_unique_off'
        db.delete_column('repchantest_book', 'version_unique_off')


        # Changing field 'Book.version_hash'
        db.alter_column('repchantest_book', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))
        # Adding field 'CollectionNotebooks.version_suspended'
        db.add_column('repchantest_collectionnotebooks', 'version_suspended',
                      self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'CollectionNotebooks.version_unique_off'
        db.delete_column('repchantest_collectionnotebooks', 'version_unique_off')


        # Changing field 'CollectionNotebooks.version_hash'
        db.alter_column('repchantest_collectionnotebooks', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))

    models = {
        'repchantest.author': {
            'Meta': {'unique_together': "(('name', 'surname'),)", 'object_name': 'Author'},
            'author_alias': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.AuthorAlias']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'repchantest.authoralias': {
            'Meta': {'unique_together': "(('name', 'version_hash', 'version_unique_off'),)", 'object_name': 'AuthorAlias'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentverpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"}),
            'version_unique_off': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
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
            'version_unique_off': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
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
            'version_unique_off': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'repchantest.notebook': {
            'Meta': {'unique_together': "(('note', 'number', 'version_hash', 'version_unique_off'),)", 'object_name': 'Notebook'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'idp': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_notebook_parentpk'", 'null': 'True', 'to': "orm['repchantest.Notebook']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_notebook_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Notebook']"}),
            'version_unique_off': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'repchantest.page': {
            'Meta': {'unique_together': "(('book', 'page_number', 'version_hash', 'version_date', 'version_unique_off'),)", 'object_name': 'Page'},
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
            'version_unique_off': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
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
            'version_unique_off': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['repchantest']