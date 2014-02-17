# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GeoIP.security'
        db.add_column(u'api_geoip', 'security',
                      self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=80),
                      keep_default=False)

        # Adding field 'GeoIP.isEnterprise'
        db.add_column(u'api_geoip', 'isEnterprise',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GeoIP.security'
        db.delete_column(u'api_geoip', 'security')

        # Deleting field 'GeoIP.isEnterprise'
        db.delete_column(u'api_geoip', 'isEnterprise')


    models = {
        u'api.geoip': {
            'Meta': {'object_name': 'GeoIP'},
            'bssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'datasrc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'isEnterprise': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'lng': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'loc': ('django.db.models.fields.CharField', [], {'default': "'No location found!'", 'max_length': '300'}),
            'rating': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ratings.Rating']", 'null': 'True'}),
            'remote_addr': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'security': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '80'}),
            'ssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        },
        u'ratings.rating': {
            'Meta': {'object_name': 'Rating'},
            'bot_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bot_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'date': ('django.db.models.fields.IntegerField', [], {'default': '16118', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_score': ('django.db.models.fields.IntegerField', [], {}),
            'spam_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'spam_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unexp_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unexp_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['api']