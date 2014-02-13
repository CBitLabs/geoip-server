# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'IpEvents', fields ['ip']
        db.create_index(u'ratings_ipevents', ['ip'])

        # Adding index on 'IpEvents', fields ['date']
        db.create_index(u'ratings_ipevents', ['date'])

        # Adding field 'Rating.date'
        db.add_column(u'ratings_rating', 'date',
                      self.gf('django.db.models.fields.IntegerField')(default=16114, db_index=True),
                      keep_default=False)

        # Adding index on 'Rating', fields ['bssid']
        db.create_index(u'ratings_rating', ['bssid'])


    def backwards(self, orm):
        # Removing index on 'Rating', fields ['bssid']
        db.delete_index(u'ratings_rating', ['bssid'])

        # Removing index on 'IpEvents', fields ['date']
        db.delete_index(u'ratings_ipevents', ['date'])

        # Removing index on 'IpEvents', fields ['ip']
        db.delete_index(u'ratings_ipevents', ['ip'])

        # Deleting field 'Rating.date'
        db.delete_column(u'ratings_rating', 'date')


    models = {
        u'ratings.ipevents': {
            'Meta': {'object_name': 'IpEvents'},
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