# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MapLayer'
        db.create_table('careerlocation_maplayer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('legend', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('careerlocation', ['MapLayer'])

        # Adding model 'ActorQuestion'
        db.create_table('careerlocation_actorquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('careerlocation', ['ActorQuestion'])

        # Adding model 'Actor'
        db.create_table('careerlocation_actor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('profile', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('left', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('top', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('careerlocation', ['Actor'])

        # Adding M2M table for field questions on 'Actor'
        db.create_table('careerlocation_actor_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('actor', models.ForeignKey(orm['careerlocation.actor'], null=False)),
            ('actorquestion', models.ForeignKey(orm['careerlocation.actorquestion'], null=False))
        ))
        db.create_unique('careerlocation_actor_questions', ['actor_id', 'actorquestion_id'])

        # Adding model 'ActorResponse'
        db.create_table('careerlocation_actorresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actor_state_user', to=orm['auth.User'])),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['careerlocation.Actor'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['careerlocation.ActorQuestion'])),
            ('long_response', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('careerlocation', ['ActorResponse'])

        # Adding model 'CareerLocationState'
        db.create_table('careerlocation_careerlocationstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='career_location_state', to=orm['auth.User'])),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('careerlocation', ['CareerLocationState'])

        # Adding M2M table for field layers on 'CareerLocationState'
        db.create_table('careerlocation_careerlocationstate_layers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('careerlocationstate', models.ForeignKey(orm['careerlocation.careerlocationstate'], null=False)),
            ('maplayer', models.ForeignKey(orm['careerlocation.maplayer'], null=False))
        ))
        db.create_unique('careerlocation_careerlocationstate_layers', ['careerlocationstate_id', 'maplayer_id'])

        # Adding M2M table for field actors on 'CareerLocationState'
        db.create_table('careerlocation_careerlocationstate_actors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('careerlocationstate', models.ForeignKey(orm['careerlocation.careerlocationstate'], null=False)),
            ('actor', models.ForeignKey(orm['careerlocation.actor'], null=False))
        ))
        db.create_unique('careerlocation_careerlocationstate_actors', ['careerlocationstate_id', 'actor_id'])

        # Adding M2M table for field responses on 'CareerLocationState'
        db.create_table('careerlocation_careerlocationstate_responses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('careerlocationstate', models.ForeignKey(orm['careerlocation.careerlocationstate'], null=False)),
            ('actorresponse', models.ForeignKey(orm['careerlocation.actorresponse'], null=False))
        ))
        db.create_unique('careerlocation_careerlocationstate_responses', ['careerlocationstate_id', 'actorresponse_id'])

        # Adding model 'CareerLocationBlock'
        db.create_table('careerlocation_careerlocationblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('base_layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['careerlocation.MapLayer'])),
            ('view', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('careerlocation', ['CareerLocationBlock'])


    def backwards(self, orm):
        
        # Deleting model 'MapLayer'
        db.delete_table('careerlocation_maplayer')

        # Deleting model 'ActorQuestion'
        db.delete_table('careerlocation_actorquestion')

        # Deleting model 'Actor'
        db.delete_table('careerlocation_actor')

        # Removing M2M table for field questions on 'Actor'
        db.delete_table('careerlocation_actor_questions')

        # Deleting model 'ActorResponse'
        db.delete_table('careerlocation_actorresponse')

        # Deleting model 'CareerLocationState'
        db.delete_table('careerlocation_careerlocationstate')

        # Removing M2M table for field layers on 'CareerLocationState'
        db.delete_table('careerlocation_careerlocationstate_layers')

        # Removing M2M table for field actors on 'CareerLocationState'
        db.delete_table('careerlocation_careerlocationstate_actors')

        # Removing M2M table for field responses on 'CareerLocationState'
        db.delete_table('careerlocation_careerlocationstate_responses')

        # Deleting model 'CareerLocationBlock'
        db.delete_table('careerlocation_careerlocationblock')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'careerlocation.actor': {
            'Meta': {'object_name': 'Actor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'left': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['careerlocation.ActorQuestion']", 'null': 'True', 'blank': 'True'}),
            'top': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'careerlocation.actorquestion': {
            'Meta': {'object_name': 'ActorQuestion'},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'careerlocation.actorresponse': {
            'Meta': {'object_name': 'ActorResponse'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['careerlocation.Actor']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['careerlocation.ActorQuestion']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor_state_user'", 'to': "orm['auth.User']"})
        },
        'careerlocation.careerlocationblock': {
            'Meta': {'object_name': 'CareerLocationBlock'},
            'base_layer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['careerlocation.MapLayer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'view': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'careerlocation.careerlocationstate': {
            'Meta': {'object_name': 'CareerLocationState'},
            'actors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['careerlocation.Actor']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['careerlocation.MapLayer']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'responses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['careerlocation.ActorResponse']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'career_location_state'", 'to': "orm['auth.User']"})
        },
        'careerlocation.maplayer': {
            'Meta': {'object_name': 'MapLayer'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'legend': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'pagetree.pageblock': {
            'Meta': {'ordering': "('section', 'ordinality')", 'object_name': 'PageBlock'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'css_extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordinality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Section']"})
        },
        'pagetree.section': {
            'Meta': {'object_name': 'Section'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hierarchy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagetree.Hierarchy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['careerlocation']
