# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'IpEvents'
        db.delete_table(u'ratings_ipevents')

        # Adding model 'IpEvent'
        db.create_table(u'ratings_ipevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, db_index=True)),
            ('spam_count', self.gf('django.db.models.fields.IntegerField')()),
            ('spam_freq', self.gf('django.db.models.fields.IntegerField')()),
            ('bot_count', self.gf('django.db.models.fields.IntegerField')()),
            ('bot_freq', self.gf('django.db.models.fields.IntegerField')()),
            ('unexp_count', self.gf('django.db.models.fields.IntegerField')()),
            ('unexp_freq', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ratings', ['IpEvent'])


    def backwards(self, orm):
        # Adding model 'IpEvents'
        db.create_table(u'ratings_ipevents', (
            ('bot_freq', self.gf('django.db.models.fields.IntegerField')()),
            ('unexp_freq', self.gf('django.db.models.fields.IntegerField')()),
            ('spam_freq', self.gf('django.db.models.fields.IntegerField')()),
            ('unexp_count', self.gf('django.db.models.fields.IntegerField')()),
            ('spam_count', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bot_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ratings', ['IpEvents'])

        # Deleting model 'IpEvent'
        db.delete_table(u'ratings_ipevent')


    models = {
        u'ratings.ipevent': {
            'Meta': {'object_name': 'IpEvent'},
            'bot_count': ('django.db.models.fields.IntegerField', [], {}),
            'bot_freq': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'db_index': 'True'}),
            'spam_count': ('django.db.models.fields.IntegerField', [], {}),
            'spam_freq': ('django.db.models.fields.IntegerField', [], {}),
            'unexp_count': ('django.db.models.fields.IntegerField', [], {}),
            'unexp_freq': ('django.db.models.fields.IntegerField', [], {})
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

    complete_apps = ['ratings']