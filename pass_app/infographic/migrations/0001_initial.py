# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InfographicBlock'
        db.create_table(u'infographic_infographicblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('intro_text', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'infographic', ['InfographicBlock'])

        # Adding model 'InfographicItem'
        db.create_table(u'infographic_infographicitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label_name', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('map_area_shape', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('coordinates', self.gf('django.db.models.fields.TextField')()),
            ('infographic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['infographic.InfographicBlock'])),
        ))
        db.send_create_signal(u'infographic', ['InfographicItem'])

        # Adding model 'InfographicState'
        db.create_table(u'infographic_infographicstate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='infographic_state', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'infographic', ['InfographicState'])

        # Adding M2M table for field items on 'InfographicState'
        m2m_table_name = db.shorten_name(u'infographic_infographicstate_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('infographicstate', models.ForeignKey(orm[u'infographic.infographicstate'], null=False)),
            ('infographicitem', models.ForeignKey(orm[u'infographic.infographicitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['infographicstate_id', 'infographicitem_id'])


    def backwards(self, orm):
        # Deleting model 'InfographicBlock'
        db.delete_table(u'infographic_infographicblock')

        # Deleting model 'InfographicItem'
        db.delete_table(u'infographic_infographicitem')

        # Deleting model 'InfographicState'
        db.delete_table(u'infographic_infographicstate')

        # Removing M2M table for field items on 'InfographicState'
        db.delete_table(db.shorten_name(u'infographic_infographicstate_items'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'infographic.infographicblock': {
            'Meta': {'object_name': 'InfographicBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_text': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        u'infographic.infographicitem': {
            'Meta': {'object_name': 'InfographicItem'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'coordinates': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infographic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['infographic.InfographicBlock']"}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'label_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'map_area_shape': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'})
        },
        u'infographic.infographicstate': {
            'Meta': {'object_name': 'InfographicState'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['infographic.InfographicItem']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'infographic_state'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['infographic']