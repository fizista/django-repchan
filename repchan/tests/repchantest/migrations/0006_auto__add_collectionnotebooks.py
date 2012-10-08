# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CollectionNotebooks'
        db.create_table('repchantest_collectionnotebooks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version_parent_pk', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_collectionnotebooks_parentpk', null=True, to=orm['repchantest.CollectionNotebooks'])),
            ('version_parent_rev_pk', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='repchantest_collectionnotebooks_parentverpk', null=True, to=orm['repchantest.CollectionNotebooks'])),
            ('version_have_children', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('version_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('version_hash', self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True)),
            ('version_in_trash', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('repchantest', ['CollectionNotebooks'])

        # Adding M2M table for field notebooks on 'CollectionNotebooks'
        db.create_table('repchantest_collectionnotebooks_notebooks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collectionnotebooks', models.ForeignKey(orm['repchantest.collectionnotebooks'], null=False)),
            ('notebook', models.ForeignKey(orm['repchantest.notebook'], null=False))
        ))
        db.create_unique('repchantest_collectionnotebooks_notebooks', ['collectionnotebooks_id', 'notebook_id'])


    def backwards(self, orm):
        # Deleting model 'CollectionNotebooks'
        db.delete_table('repchantest_collectionnotebooks')

        # Removing M2M table for field notebooks on 'CollectionNotebooks'
        db.delete_table('repchantest_collectionnotebooks_notebooks')


    models = {
        'repchantest.author': {
            'Meta': {'unique_together': "(('name', 'surname'),)", 'object_name': 'Author'},
            'author_alias': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.AuthorAlias']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'repchantest.authoralias': {
            'Meta': {'unique_together': "(('name', 'version_hash'),)", 'object_name': 'AuthorAlias'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_authoralias_parentverpk'", 'null': 'True', 'to': "orm['repchantest.AuthorAlias']"})
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
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_book_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Book']"})
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
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_collectionnotebooks_parentverpk'", 'null': 'True', 'to': "orm['repchantest.CollectionNotebooks']"})
        },
        'repchantest.notebook': {
            'Meta': {'unique_together': "(('note', 'number', 'version_hash'),)", 'object_name': 'Notebook'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'version_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version_hash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'version_have_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_in_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version_parent_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_notebook_parentpk'", 'null': 'True', 'to': "orm['repchantest.Notebook']"}),
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_notebook_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Notebook']"})
        },
        'repchantest.page': {
            'Meta': {'unique_together': "(('book', 'page_number', 'version_hash', 'version_date'),)", 'object_name': 'Page'},
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
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_page_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Page']"})
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
            'version_parent_rev_pk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'repchantest_section_parentverpk'", 'null': 'True', 'to': "orm['repchantest.Section']"})
        }
    }

    complete_apps = ['repchantest']