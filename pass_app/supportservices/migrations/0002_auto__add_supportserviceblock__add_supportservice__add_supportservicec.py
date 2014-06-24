# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SupportServiceBlock'
        db.create_table(u'supportservices_supportserviceblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'supportservices', ['SupportServiceBlock'])

        # Adding model 'SupportService'
        db.create_table(u'supportservices_supportservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['supportservices.SupportServiceCategory'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'supportservices', ['SupportService'])

        # Adding model 'SupportServiceCategory'
        db.create_table(u'supportservices_supportservicecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'supportservices', ['SupportServiceCategory'])


    def backwards(self, orm):
        # Deleting model 'SupportServiceBlock'
        db.delete_table(u'supportservices_supportserviceblock')

        # Deleting model 'SupportService'
        db.delete_table(u'supportservices_supportservice')

        # Deleting model 'SupportServiceCategory'
        db.delete_table(u'supportservices_supportservicecategory')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'pagetree.pageblock': {
            'Meta': {'ordering': "('section', 'ordinality')", 'object_name': 'PageBlock'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'css_extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordinality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pagetree.Section']"})
        },
        u'pagetree.section': {
            'Meta': {'object_name': 'Section'},
            'deep_toc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hierarchy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pagetree.Hierarchy']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'show_toc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'supportservices.supportservice': {
            'Meta': {'object_name': 'SupportService'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['supportservices.SupportServiceCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'supportservices.supportserviceblock': {
            'Meta': {'object_name': 'SupportServiceBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'supportservices.supportservicecategory': {
            'Meta': {'object_name': 'SupportServiceCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['supportservices']