# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from ratings.query_manager import rating_manager
from ratings.models import Rating


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for geoip in orm.GeoIP.objects.all():
            rating = rating_manager(
                geoip.ip, geoip.bssid, geoip.ssid, geoip.lat, geoip.lng)
            geoip.rating_id = rating.id
            geoip.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
    symmetrical = True
