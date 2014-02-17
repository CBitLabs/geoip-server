# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Rating.spam_count'
        db.add_column(u'ratings_rating', 'spam_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rating.spam_freq'
        db.add_column(u'ratings_rating', 'spam_freq',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rating.bot_count'
        db.add_column(u'ratings_rating', 'bot_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rating.bot_freq'
        db.add_column(u'ratings_rating', 'bot_freq',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rating.unexp_count'
        db.add_column(u'ratings_rating', 'unexp_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Rating.unexp_freq'
        db.add_column(u'ratings_rating', 'unexp_freq',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Rating.spam_count'
        db.delete_column(u'ratings_rating', 'spam_count')

        # Deleting field 'Rating.spam_freq'
        db.delete_column(u'ratings_rating', 'spam_freq')

        # Deleting field 'Rating.bot_count'
        db.delete_column(u'ratings_rating', 'bot_count')

        # Deleting field 'Rating.bot_freq'
        db.delete_column(u'ratings_rating', 'bot_freq')

        # Deleting field 'Rating.unexp_count'
        db.delete_column(u'ratings_rating', 'unexp_count')

        # Deleting field 'Rating.unexp_freq'
        db.delete_column(u'ratings_rating', 'unexp_freq')


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
            'date': ('django.db.models.fields.IntegerField', [], {'default': '16118', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_score': ('django.db.models.fields.IntegerField', [], {}),
            'spam_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'spam_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unexp_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'unexp_freq': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['ratings']