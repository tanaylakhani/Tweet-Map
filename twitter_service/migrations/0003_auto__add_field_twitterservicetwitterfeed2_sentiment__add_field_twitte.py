# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TwitterServiceTwitterfeed2.sentiment'
        db.add_column(u'twitter_service_twitterfeed2', 'sentiment',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TwitterServiceTwitterfeed2.sentiment_score'
        db.add_column(u'twitter_service_twitterfeed2', 'sentiment_score',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=6),
                      keep_default=False)


        # Changing field 'TwitterServiceTwitterfeed2.id'
        db.alter_column(u'twitter_service_twitterfeed2', 'id', self.gf('django.db.models.fields.IntegerField')(primary_key=True))

    def backwards(self, orm):
        # Deleting field 'TwitterServiceTwitterfeed2.sentiment'
        db.delete_column(u'twitter_service_twitterfeed2', 'sentiment')

        # Deleting field 'TwitterServiceTwitterfeed2.sentiment_score'
        db.delete_column(u'twitter_service_twitterfeed2', 'sentiment_score')


        # Changing field 'TwitterServiceTwitterfeed2.id'
        db.alter_column(u'twitter_service_twitterfeed2', u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True))

    models = {
        u'twitter_service.authgroup': {
            'Meta': {'object_name': 'AuthGroup', 'db_table': "u'auth_group'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        u'twitter_service.authgrouppermissions': {
            'Meta': {'object_name': 'AuthGroupPermissions', 'db_table': "u'auth_group_permissions'", 'managed': 'False'},
            'group_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'permission_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'twitter_service.authpermission': {
            'Meta': {'object_name': 'AuthPermission', 'db_table': "u'auth_permission'", 'managed': 'False'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'twitter_service.authuser': {
            'Meta': {'object_name': 'AuthUser', 'db_table': "u'auth_user'", 'managed': 'False'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.IntegerField', [], {}),
            'is_staff': ('django.db.models.fields.IntegerField', [], {}),
            'is_superuser': ('django.db.models.fields.IntegerField', [], {}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'twitter_service.authusergroups': {
            'Meta': {'object_name': 'AuthUserGroups', 'db_table': "u'auth_user_groups'", 'managed': 'False'},
            'group_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'twitter_service.authuseruserpermissions': {
            'Meta': {'object_name': 'AuthUserUserPermissions', 'db_table': "u'auth_user_user_permissions'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'permission_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'twitter_service.djangoadminlog': {
            'Meta': {'object_name': 'DjangoAdminLog', 'db_table': "u'django_admin_log'", 'managed': 'False'},
            'action_flag': ('django.db.models.fields.IntegerField', [], {}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {}),
            'change_message': ('django.db.models.fields.TextField', [], {}),
            'content_type_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'object_repr': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'twitter_service.djangocontenttype': {
            'Meta': {'object_name': 'DjangoContentType', 'db_table': "u'django_content_type'", 'managed': 'False'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'twitter_service.djangosession': {
            'Meta': {'object_name': 'DjangoSession', 'db_table': "u'django_session'", 'managed': 'False'},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        },
        u'twitter_service.southmigrationhistory': {
            'Meta': {'object_name': 'SouthMigrationhistory', 'db_table': "u'south_migrationhistory'", 'managed': 'False'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'applied': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'migration': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'twitter_service.twitterservicetwitterfeed2': {
            'Meta': {'object_name': 'TwitterServiceTwitterfeed2', 'db_table': "u'twitter_service_twitterfeed2'"},
            'date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "u'Date'"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sentiment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sentiment_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '6'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "u'Text'"}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "u'UserID'"}),
            'x': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "u'X'"}),
            'y': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "u'Y'"})
        }
    }

    complete_apps = ['twitter_service']