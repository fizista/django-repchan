# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AuthorAlias'
        db.create_table('repchantest_authoralias', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('repchantest', ['AuthorAlias'])

        # Adding model 'Author'
        db.create_table('repchantest_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('author_alias', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repchantest.AuthorAlias'], null=True, blank=True)),
        ))
        db.send_create_signal('repchantest', ['Author'])

        # Adding unique constraint on 'Author', fields ['name', 'surname']
        db.create_unique('repchantest_author', ['name', 'surname'])

        # Adding model 'Section'
        db.create_table('repchantest_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('repchantest', ['Section'])

        # Adding model 'Chapter'
        db.create_table('repchantest_chapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('repchantest', ['Chapter'])

        # Adding model 'Book'
        db.create_table('repchantest_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repchantest.Author'])),
            ('log', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal('repchantest', ['Book'])

        # Adding model 'Page'
        db.create_table('repchantest_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_number', self.gf('django.db.models.fields.IntegerField')()),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repchantest.Book'])),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repchantest.Chapter'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repchantest.Section'])),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('repchantest', ['Page'])

        # Adding unique constraint on 'Page', fields ['book', 'page_number']
        db.create_unique('repchantest_page', ['book_id', 'page_number'])


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['book', 'page_number']
        db.delete_unique('repchantest_page', ['book_id', 'page_number'])

        # Removing unique constraint on 'Author', fields ['name', 'surname']
        db.delete_unique('repchantest_author', ['name', 'surname'])

        # Deleting model 'AuthorAlias'
        db.delete_table('repchantest_authoralias')

        # Deleting model 'Author'
        db.delete_table('repchantest_author')

        # Deleting model 'Section'
        db.delete_table('repchantest_section')

        # Deleting model 'Chapter'
        db.delete_table('repchantest_chapter')

        # Deleting model 'Book'
        db.delete_table('repchantest_book')

        # Deleting model 'Page'
        db.delete_table('repchantest_page')


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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'repchantest.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repchantest.Section']"})
        },
        'repchantest.section': {
            'Meta': {'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['repchantest']