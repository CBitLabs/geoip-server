# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PrefReport'
        db.create_table(u'api_prefreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('ssid', self.gf('django.db.models.fields.CharField')(default='', max_length=80, db_index=True)),
        ))
        db.send_create_signal(u'api', ['PrefReport'])


    def backwards(self, orm):
        # Deleting model 'PrefReport'
        db.delete_table(u'api_prefreport')


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
        u'api.prefreport': {
            'Meta': {'object_name': 'PrefReport'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        },
        u'ratings.rating': {
            'Meta': {'object_name': 'Rating'},
            'bot_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bot_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'date': ('django.db.models.fields.IntegerField', [], {'default': '16168', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_infected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'raw_score': ('django.db.models.fields.IntegerField', [], {}),
            'spam_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'spam_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unexp_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unexp_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['api']