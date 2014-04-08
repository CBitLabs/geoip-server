# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Rating.is_valid'
        db.add_column(u'ratings_rating', 'is_valid',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Rating.is_valid'
        db.delete_column(u'ratings_rating', 'is_valid')


    models = {
        u'ratings.ipevent': {
            'Meta': {'object_name': 'IpEvent'},
            'bot_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bot_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'db_index': 'True'}),
            'spam_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'spam_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unexp_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unexp_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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

    complete_apps = ['ratings']