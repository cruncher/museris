# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from progress.bar import Bar
import re
import requests
from ...models import (
    Institution, DataObject, DataObjectImage, DataObjectProperty,
    DataObjectLatLong, Person, PersonProperty, DataObjectPerson)
from requests.exceptions import TooManyRedirects


CLEAN_KEYS = re.compile(r'\s*:\s*$')
FLOATS = re.compile(r'\d+\.\d+')
PEOPLE_ID = re.compile(r'SGP/Consultation\.aspx\?Id=(\d+)')

START_ID = 1
END_ID = 187000


def scrape(start, end):
    """
        Scrapes museris.lausanne.ch based on the start and end ID of the remote object.
        Populates the local database with DataObjects and Person data models, and assigns
        them their metadata objects (images, properties, coords).
    """

    def clean(v):
        "cleans a value (key or value for object properties)"
        ret = []

        # People data objects can be returned unchanged
        if type(v) == Person:
            return v
        # clean up strings and truncate them
        for s in v.strings:
            ret.append(CLEAN_KEYS.sub('', s)[:1024])
        # If we have a single string, return it directly
        # otherwise, return an array of strings
        if 1 == len(ret):
            return ret[0][:1024]
        return ret

    def get_person(person_id):
        """
            Rerturns a Person data model instsance based on its ID.
            If it exists already, simply return it. Otherwise request
            and extract the data, then build and save the instance,
            and finally return it
        """

        try:
            return Person.objects.get(object_id=int(person_id))
        except Person.DoesNotExist:
            url = 'https://museris.lausanne.ch/SGP/Consultation.aspx?Id=%d' % person_id
            resp = requests.get(url)
            soup = BeautifulSoup(resp.content)
            table = soup.select('div#body table')[0]
            keys = table.select('td.infoname')
            values = table.select('td.infos')

            # make sure we have data
            if not len(keys) or not len(values):
                return None

            if len(keys) != len(values):
                return None

            # Extract document meta info
            metas = (dict(zip(
                map(clean, keys),
                map(clean, values)
            )))

            p = Person.objects.create(
                object_id=int(person_id),
                name=('%s %s' % (metas.get(u'Prénom', ''), metas.get(u'Nom ou appellation', ''))).strip()
            )
            # Assign meta properties
            for k, v in metas.iteritems():
                if list == type(v):
                    for val in v:
                        PersonProperty.objects.create(person=p, key=k, value=val)
                else:
                    PersonProperty.objects.create(person=p, key=k, value=v)
            return p



    bar = Bar('Scraping', index=start, max=end, suffix='%(index)d/%(max)d (%(percent)d%%) ETA: %(eta_td)s')
    for pid in range(start, end + 1):
        bar.next()
        url = 'https://musees.lausanne.ch/SGCM/Consultation.aspx?id=%d' % pid
        try:
            resp = requests.get(url)
        except TooManyRedirects:
            print ' error fetching', pid
            continue
        else:
            soup = BeautifulSoup(resp.content)

        try:
            # div#body has all the interesting stuff
            table = soup.select('div#body table')[0]
            keys = table.select('td.infoname')
            values = table.select('td.infos')

            # make sure we have data
            if not len(keys) or not len(values):
                print ' no keys or values for %d' % pid
                continue

            if len(keys) != len(values):
                print ' unbalanced keys / values for %d' % pid
                continue

            # Look for people: convert hyperlinks with People IDs to
            # actual People data models and store these instead.
            for i, v in enumerate(values[:]):
                if v.select('a') and '/SGP/' in v.select('a')[0].attrs.get('href'):
                    ids = PEOPLE_ID.findall(v.select('a')[0].attrs.get('href'))
                    if ids:
                        values[i] = get_person(int(ids[0]))

            # Extract document meta info
            metas = (dict(zip(
                map(clean, keys),
                map(clean, values)
            )))


            # Duplicate data, drop this
            if 'Description sommaire (auto)' in metas:
                del(metas['Description sommaire (auto)'])

            # We need an Institution (museum) because we're
            # going to denormalize this key and use it as a
            # filter
            if not metas.get('Institution'):
                print ' missing institution in %d' % pid
                continue

            # Image(s).
            imgs = []
            for img in table.select('a img'):
                imgs.append(img.attrs.get('src').replace('/Vignette/', '/ImgDeg/').replace('_2.', '_1.'))

            # latlong
            geo = []
            for iframe in table.select('iframe#framegeo'):
                geo += map(float, FLOATS.findall(iframe.attrs.get('src')))

            # All done, make sure we have an Institution for this piece
            i, _ = Institution.objects.get_or_create(name=metas.get('Institution'))

            # Create the main object
            obj = DataObject.objects.create(
                object_id=pid,
                institution=i
            )

            # Assign meta properties
            for k, v in metas.iteritems():
                # Lists: simply create multiple properties with the same key
                if list == type(v):
                    for val in v:
                        DataObjectProperty.objects.create(data_object=obj, key=k, value=val)
                # People (authors, ...). Create a M2M with a role linking the person to the
                # object
                elif Person == type(v):
                    DataObjectPerson.objects.create(
                        person=v,
                        data_object=obj,
                        role=k
                    )
                # A simple object property
                else:
                    DataObjectProperty.objects.create(data_object=obj, key=k, value=v)

            # Images. Note that images are not downloaded, we only save their URL.
            # A separate management command will download images and assign them
            # to the DataObjectImage objects.
            for i in imgs:
                DataObjectImage.objects.create(data_object=obj, image_url=i)

            # ... and lat / lng, if any.
            while len(geo) >= 2:
                lat, lng = geo.pop(0), geo.pop(0)
                DataObjectLatLong.objects.create(data_object=obj, latitude=lat, longitude=lng)

        # No div#body tag?
        except IndexError:
            print ' failed', pid
            continue

    bar.finish()


class Command(BaseCommand):
    help = "Scrapes the https://museris.lausanne.ch/ website, extracting all Objects and People"

    def handle(self, *args, **options):
        if len(args) == 2:
            scrape(int(args[0]), 1 + int(args[1]))
        elif len(args) == 1:
            scrape(int(args[0]), 1 + int(args[0]))
        else:
            try:
                start = 2 + DataObject.objects.order_by('-pk')[0].pk
            except IndexError:
                start = START_ID
            scrape(start, END_ID)
