# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Delegate'
        db.create_table(u'quiz_delegate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organisation', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sector', self.gf('django.db.models.fields.CharField')(default='NS', max_length=2)),
            ('quiz_answers', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=100)),
            ('quiz_result', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'quiz', ['Delegate'])

        # Adding model 'Printer'
        db.create_table(u'quiz_printer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'quiz', ['Printer'])

        # Adding model 'Badge'
        db.create_table(u'quiz_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('print_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('delegate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Delegate'])),
            ('printer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Printer'])),
            ('printed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'quiz', ['Badge'])


    def backwards(self, orm):
        # Deleting model 'Delegate'
        db.delete_table(u'quiz_delegate')

        # Deleting model 'Printer'
        db.delete_table(u'quiz_printer')

        # Deleting model 'Badge'
        db.delete_table(u'quiz_badge')


    models = {
        u'quiz.badge': {
            'Meta': {'object_name': 'Badge'},
            'delegate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Delegate']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'print_time': ('django.db.models.fields.DateTimeField', [], {}),
            'printed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'printer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quiz.Printer']"})
        },
        u'quiz.delegate': {
            'Meta': {'object_name': 'Delegate'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quiz_answers': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '100'}),
            'quiz_result': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sector': ('django.db.models.fields.CharField', [], {'default': "'NS'", 'max_length': '2'})
        },
        u'quiz.printer': {
            'Meta': {'object_name': 'Printer'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['quiz']