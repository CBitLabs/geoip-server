# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IpEvents'
        db.create_table(u'ratings_ipevents', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.IntegerField')()),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('spam_count', self.gf('django.db.models.fields.IntegerField')()),
            ('spam_freq', self.gf('django.db.models.fields.IntegerField')()),
            ('bot_count', self.gf('django.db.models.fields.IntegerField')()),
            ('bot_freq', self.gf('django.db.models.fields.IntegerField')()),
            ('unexp_count', self.gf('django.db.models.fields.IntegerField')()),
            ('unexp_freq', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ratings', ['IpEvents'])

        # Adding model 'Rating'
        db.create_table(u'ratings_rating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('raw_score', self.gf('django.db.models.fields.IntegerField')()),
            ('bssid', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'ratings', ['Rating'])


    def backwards(self, orm):
        # Deleting model 'IpEvents'
        db.delete_table(u'ratings_ipevents')

        # Deleting model 'Rating'
        db.delete_table(u'ratings_rating')


    models = {
        u'ratings.ipevents': {
            'Meta': {'object_name': 'IpEvents'},
            'bot_count': ('django.db.models.fields.IntegerField', [], {}),
            'bot_freq': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'spam_count': ('django.db.models.fields.IntegerField', [], {}),
            'spam_freq': ('django.db.models.fields.IntegerField', [], {}),
            'unexp_count': ('django.db.models.fields.IntegerField', [], {}),
            'unexp_freq': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ratings.rating': {
            'Meta': {'object_name': 'Rating'},
            'bssid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_score': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['ratings']