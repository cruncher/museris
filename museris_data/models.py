# -*- coding: utf-8 -*-
from django.db import models
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests
import os


class Institution(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class DataObject(models.Model):
    object_id = models.IntegerField(primary_key=True)
    institution = models.ForeignKey(Institution, related_name='data_objects')

    def __unicode__(self):
        for p in self.properties.filter(key__in=(u'Désignation spécifique', u'Titre donné par l\'artiste', 'Intervention artistique (pour-cent culturel, etc.)', 'Description')):
            return p.value
        return u'#%d' % self.object_id


class Person(models.Model):
    object_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'People'


class PersonProperty(models.Model):
    person = models.ForeignKey(Person, related_name='properties')
    key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    value = models.CharField(max_length=1024, blank=True, null=True)

    def __unicode__(self):
        return self.key



def image_upload_to(instance, filename):
    return 'ul/img/%s/%d/%d.%s' % (
        slugify(instance.data_object.institution.name),
        instance.data_object.pk,
        instance.pk,
        'jpg'
    )


class DataObjectImage(models.Model):
    data_object = models.ForeignKey(DataObject, related_name='images')
    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def url_to_img(self):
        if os.path.splitext(self.image_url)[0].endswith('_2'):
            self.image_url = self.image_url.replace('_2.', '_1.')

        resp = requests.get(self.image_url)
        if resp.status_code == requests.codes.ok:

            ext = os.path.splitext(self.image_url)[-1].lower()
            self.image.save('%d%s' % (self.pk, ext), ContentFile(resp.content))

        else:
            print ' Error on obj # %d: %s' % (self.data_object.pk, self.image_url)



class DataObjectProperty(models.Model):
    data_object = models.ForeignKey(DataObject, related_name='properties')
    key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    value = models.CharField(max_length=1024, blank=True, null=True)

    def __unicode__(self):
        return self.key


class DataObjectLatLong(models.Model):
    data_object = models.ForeignKey(DataObject, related_name='coords')
    latitude = models.DecimalField(max_digits=15, decimal_places=12)
    longitude = models.DecimalField(max_digits=15, decimal_places=12)


class DataObjectPerson(models.Model):
    data_object = models.ForeignKey(DataObject, related_name='people')
    person = models.ForeignKey(Person, related_name='data_objects')
    role = models.CharField(max_length=255, blank=True, null=True)
