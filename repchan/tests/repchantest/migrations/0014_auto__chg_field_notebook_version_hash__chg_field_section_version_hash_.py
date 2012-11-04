# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Notebook.version_hash'
        db.alter_column('repchantest_notebook', 'version_hash', self.gf('django.db.models.fields.TextField')(max_length=100))

        # Changing field 'Section.version_hash'
        db.alter_column('repchantest_section', 'version_hash', self.gf('django.db.models.fields.TextField')(max_length=256))

        # Changing field 'AuthorAlias.version_hash'
        db.alter_column('repchantest_authoralias', 'version_hash', self.gf('django.db.models.fields.TextField')(max_length=256))

        # Changing field 'Page.version_hash'
        db.alter_column('repchantest_page', 'version_hash', self.gf('django.db.models.fields.TextField')(max_length=512))

        # Changing field 'Book.version_hash'
        db.alter_column('repchantest_book', 'version_hash', self.gf('django.db.models.fields.TextField')(max_length=64))

        # Changing field 'CollectionNotebooks.version_hash'
        db.alter_column('repchantest_collectionnotebooks', 'version_hash', self.gf('django.db.models.fields.TextField')(max_length=256))

    def backwards(self, orm):

        # Changing field 'Notebook.version_hash'
        db.alter_column('repchantest_notebook', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Section.version_hash'
        db.alter_column('repchantest_section', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=256))

        # Changing field 'AuthorAlias.version_hash'
        db.alter_column('repchantest_authoralias', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=256))

        # Changing field 'Page.version_hash'
        db.alter_column('repchantest_page', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=512))

        # Changing field 'Book.version_hash'
        db.alter_column('repchantest_book', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=64))

        # Changing field 'CollectionNotebooks.version_hash'
        db.alter_column('repchantest_collectionnotebooks', 'version_hash', self.gf('django.db.models.fields.CharField')(max_length=256))

    models = {
        'repchantest.author': {
            'Meta': {'unique_together': "(('name', 'surname'),)", 'object_name': 'Author'},
            'author_alias': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.AuthorAlias']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'repchantest.authoralias': {
            'Meta': {'unique_together': "(('name', 'version_hash', 'version_unique_on'),)", 'object_name': 'AuthorAlias'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentverpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"}),
            'version_unique_on': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.book': {
            'Meta': {'unique_together': '()', 'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_book_parentpk'", 'null': 'True', 'to': "orm['repchantest.Book']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_book_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Book']"}),
            'version_unique_on': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
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
            'version_hash': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_collectionnotebooks_parentpk'", 'null': 'True', 'to': "orm['repchantest.CollectionNotebooks']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_collectionnotebooks_parentverpk'", 'null': 'True', 'to': "orm['repchantest.CollectionNotebooks']"}),
            'version_unique_on': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.notebook': {
            'Meta': {'unique_together': "(('note', 'number', 'version_hash', 'version_unique_on'),)", 'object_name': 'Notebook'},
            'alias': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '150'}),
            'idp': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_notebook_parentpk'", 'null': 'True', 'to': "orm['repchantest.Notebook']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_notebook_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Notebook']"}),
            'version_unique_on': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.page': {
            'Meta': {'unique_together': "(('book', 'page_number', 'version_hash', 'version_date', 'version_unique_on'),)", 'object_name': 'Page'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Book']"}),
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Chapter']"}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'page_number': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Section']"}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_page_parentpk'", 'null': 'True', 'to': "orm['repchantest.Page']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_page_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Page']"}),
            'version_unique_on': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        'repchantest.section': {
            'Meta': {'unique_together': '()', 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_section_parentpk'", 'null': 'True', 'to': "orm['repchantest.Section']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_section_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Section']"}),
            'version_unique_on': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['repchantest']