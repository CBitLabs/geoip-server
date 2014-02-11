# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GeoIP'
        db.create_table(u'api_geoip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('loc', self.gf('django.db.models.fields.CharField')(default='No location found!', max_length=300)),
            ('bssid', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('ssid', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('remote_addr', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('datasrc', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'api', ['GeoIP'])


    def backwards(self, orm):
        # Deleting model 'GeoIP'
        db.delete_table(u'api_geoip')


    models = {
        u'api.geoip': {
            'Meta': {'object_name': 'GeoIP'},
            'bssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'datasrc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'loc': ('django.db.models.fields.CharField', [], {'default': "'No location found!'", 'max_length': '300'}),
            'remote_addr': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'ssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        }
    }

    complete_apps = ['api']