# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'GeoIP.rating'
        db.alter_column(u'api_geoip', 'rating_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Rating'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'GeoIP.rating'
        raise RuntimeError("Cannot reverse this migration. 'GeoIP.rating' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'GeoIP.rating'
        db.alter_column(u'api_geoip', 'rating_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Rating']))

    models = {
        u'api.geoip': {
            'Meta': {'object_name': 'GeoIP'},
            'bssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'datasrc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'loc': ('django.db.models.fields.CharField', [], {'default': "'No location found!'", 'max_length': '300'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ratings.Rating']", 'null': 'True'}),
            'remote_addr': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'ssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        },
        u'ratings.rating': {
            'Meta': {'object_name': 'Rating'},
            'bssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'date': ('django.db.models.fields.IntegerField', [], {'default': '16114', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_score': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['api']