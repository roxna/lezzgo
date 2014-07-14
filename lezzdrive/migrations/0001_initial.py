# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rider'
        db.create_table(u'lezzdrive_rider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='Male', max_length=6)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='650-111-2222', max_length=12, null=True, blank=True)),
            ('birth_year', self.gf('django.db.models.fields.IntegerField')(default=1985, max_length=4, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.IntegerField')(default=94123, max_length=5, null=True, blank=True)),
            ('profile_pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'lezzdrive', ['Rider'])

        # Adding M2M table for field groups on 'Rider'
        m2m_table_name = db.shorten_name(u'lezzdrive_rider_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rider', models.ForeignKey(orm[u'lezzdrive.rider'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['rider_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Rider'
        m2m_table_name = db.shorten_name(u'lezzdrive_rider_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rider', models.ForeignKey(orm[u'lezzdrive.rider'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['rider_id', 'permission_id'])

        # Adding model 'Driver'
        db.create_table(u'lezzdrive_driver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_accidents', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('num_rides_given', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('rider', self.gf('django.db.models.fields.related.OneToOneField')(related_name='driver_profile', unique=True, to=orm['lezzdrive.Rider'])),
        ))
        db.send_create_signal(u'lezzdrive', ['Driver'])

        # Adding model 'Passenger'
        db.create_table(u'lezzdrive_passenger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_rides_taken', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('rider', self.gf('django.db.models.fields.related.OneToOneField')(related_name='passenger_profile', unique=True, to=orm['lezzdrive.Rider'])),
        ))
        db.send_create_signal(u'lezzdrive', ['Passenger'])

        # Adding model 'Ride'
        db.create_table(u'lezzdrive_ride', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('driver', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='as_driver', null=True, to=orm['lezzdrive.Rider'])),
            ('departure_city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('arrival_city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('departure_date', self.gf('django.db.models.fields.DateField')()),
            ('departure_time', self.gf('django.db.models.fields.TimeField')()),
            ('price_per_seat', self.gf('django.db.models.fields.IntegerField')()),
            ('num_seats_available', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('car', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=200, null=True)),
            ('no_smoking', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_pets', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ladies_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('valid_docs', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'lezzdrive', ['Ride'])

        # Adding M2M table for field passenger on 'Ride'
        m2m_table_name = db.shorten_name(u'lezzdrive_ride_passenger')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ride', models.ForeignKey(orm[u'lezzdrive.ride'], null=False)),
            ('rider', models.ForeignKey(orm[u'lezzdrive.rider'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ride_id', 'rider_id'])


    def backwards(self, orm):
        # Deleting model 'Rider'
        db.delete_table(u'lezzdrive_rider')

        # Removing M2M table for field groups on 'Rider'
        db.delete_table(db.shorten_name(u'lezzdrive_rider_groups'))

        # Removing M2M table for field user_permissions on 'Rider'
        db.delete_table(db.shorten_name(u'lezzdrive_rider_user_permissions'))

        # Deleting model 'Driver'
        db.delete_table(u'lezzdrive_driver')

        # Deleting model 'Passenger'
        db.delete_table(u'lezzdrive_passenger')

        # Deleting model 'Ride'
        db.delete_table(u'lezzdrive_ride')

        # Removing M2M table for field passenger on 'Ride'
        db.delete_table(db.shorten_name(u'lezzdrive_ride_passenger'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lezzdrive.driver': {
            'Meta': {'object_name': 'Driver'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_accidents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'num_rides_given': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'rider': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'driver_profile'", 'unique': 'True', 'to': u"orm['lezzdrive.Rider']"})
        },
        u'lezzdrive.passenger': {
            'Meta': {'object_name': 'Passenger'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_rides_taken': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'rider': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'passenger_profile'", 'unique': 'True', 'to': u"orm['lezzdrive.Rider']"})
        },
        u'lezzdrive.ride': {
            'Meta': {'object_name': 'Ride'},
            'arrival_city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'car': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True'}),
            'departure_city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'departure_date': ('django.db.models.fields.DateField', [], {}),
            'departure_time': ('django.db.models.fields.TimeField', [], {}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'as_driver'", 'null': 'True', 'to': u"orm['lezzdrive.Rider']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ladies_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_pets': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_smoking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_seats_available': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'passenger': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'as_passenger'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['lezzdrive.Rider']"}),
            'price_per_seat': ('django.db.models.fields.IntegerField', [], {}),
            'valid_docs': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'lezzdrive.rider': {
            'Meta': {'object_name': 'Rider'},
            'birth_year': ('django.db.models.fields.IntegerField', [], {'default': '1985', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '6'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "'650-111-2222'", 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'profile_pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'default': '94123', 'max_length': '5', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lezzdrive']