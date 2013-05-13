# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CareerLocationStrategyBlock'
        db.create_table('careerlocation_careerlocationstrategyblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('base_layer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['careerlocation.MapLayer'])),
            ('view', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('careerlocation', ['CareerLocationStrategyBlock'])

        # Adding M2M table for field optional_layers on 'CareerLocationStrategyBlock'
        db.create_table('careerlocation_careerlocationstrategyblock_optional_layers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('careerlocationstrategyblock', models.ForeignKey(orm['careerlocation.careerlocationstrategyblock'], null=False)),
            ('maplayer', models.ForeignKey(orm['careerlocation.maplayer'], null=False))
        ))
        db.create_unique('careerlocation_careerlocationstrategyblock_optional_layers', ['careerlocationstrategyblock_id', 'maplayer_id'])

        # Adding model 'Strategy'
        db.create_table('careerlocation_strategy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ordinal', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('pros', self.gf('django.db.models.fields.TextField')()),
            ('cons', self.gf('django.db.models.fields.TextField')()),
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('example', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('careerlocation', ['Strategy'])

        # Adding field 'CareerLocationState.strategy_selected'
        db.add_column('careerlocation_careerlocationstate', 'strategy_selected', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='strategy_selected', null=True, to=orm['careerlocation.Strategy']), keep_default=False)

        # Adding M2M table for field strategies_viewed on 'CareerLocationState'
        db.create_table('careerlocation_careerlocationstate_strategies_viewed', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('careerlocationstate', models.ForeignKey(orm['careerlocation.careerlocationstate'], null=False)),
            ('strategy', models.ForeignKey(orm['careerlocation.strategy'], null=False))
        ))
        db.create_unique('careerlocation_careerlocationstate_strategies_viewed', ['careerlocationstate_id', 'strategy_id'])


    def backwards(self, orm):
        
        # Deleting model 'CareerLocationStrategyBlock'
        db.delete_table('careerlocation_careerlocationstrategyblock')

        # Removing M2M table for field optional_layers on 'CareerLocationStrategyBlock'
        db.delete_table('careerlocation_careerlocationstrategyblock_optional_layers')

        # Deleting model 'Strategy'
        db.delete_table('careerlocation_strategy')

        # Deleting field 'CareerLocationState.strategy_selected'
        db.delete_column('careerlocation_careerlocationstate', 'strategy_selected_id')

        # Removing M2M table for field strategies_viewed on 'CareerLocationState'
        db.delete_table('careerlocation_careerlocationstate_strategies_viewed')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 19, 11, 20, 0, 990565)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 19, 11, 20, 0, 990482)'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'optional_layers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'optional_layers'", 'symmetrical': 'False', 'to': "orm['careerlocation.MapLayer']"}),
            'view': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'careerlocation.careerlocationstate': {
            'Meta': {'object_name': 'CareerLocationState'},
            'actors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['careerlocation.Actor']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['careerlocation.MapLayer']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'practice_location_column': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'practice_location_row': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'responses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['careerlocation.ActorResponse']", 'null': 'True', 'blank': 'True'}),
            'strategies_viewed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'strategies_viewed'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['careerlocation.Strategy']"}),
            'strategy_selected': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'strategy_selected'", 'null': 'True', 'to': "orm['careerlocation.Strategy']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'career_location_state'", 'to': "orm['auth.User']"})
        },
        'careerlocation.careerlocationstrategyblock': {
            'Meta': {'object_name': 'CareerLocationStrategyBlock'},
            'base_layer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['careerlocation.MapLayer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optional_layers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'strategy_optional_layers'", 'symmetrical': 'False', 'to': "orm['careerlocation.MapLayer']"}),
            'view': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'careerlocation.careerlocationsummaryblock': {
            'Meta': {'object_name': 'CareerLocationSummaryBlock'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'careerlocation.maplayer': {
            'Meta': {'object_name': 'MapLayer'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'legend': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'transparency': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'z_index': ('django.db.models.fields.IntegerField', [], {'default': '999'})
        },
        'careerlocation.strategy': {
            'Meta': {'object_name': 'Strategy'},
            'cons': ('django.db.models.fields.TextField', [], {}),
            'example': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordinal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pros': ('django.db.models.fields.TextField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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