# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GeoIP.rating'
        orm["ratings.Rating"].objects.get_or_create(id=0, raw_score=0)
        db.add_column(u'api_geoip', 'rating',
                      self.gf('django.db.models.fields.related.ForeignKey')(
                          default=0, to=orm['ratings.Rating']),
                      keep_default=False)

        # Adding index on 'GeoIP', fields ['bssid']
        db.create_index(u'api_geoip', ['bssid'])

        # Adding index on 'GeoIP', fields ['ssid']
        db.create_index(u'api_geoip', ['ssid'])

    def backwards(self, orm):
        # Removing index on 'GeoIP', fields ['ssid']
        db.delete_index(u'api_geoip', ['ssid'])

        # Removing index on 'GeoIP', fields ['bssid']
        db.delete_index(u'api_geoip', ['bssid'])

        # Deleting field 'GeoIP.rating'
        db.delete_column(u'api_geoip', 'rating_id')

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
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ratings.Rating']"}),
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
