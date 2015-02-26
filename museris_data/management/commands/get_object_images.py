# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from progress.bar import Bar
from ...models import DataObjectImage


class Command(BaseCommand):
    help = "Downloads images and assigns them to DataObjectImage objects"

    def handle(self, *args, **options):
        images = DataObjectImage.objects.filter(image='', image_url__isnull=False)
        bar = Bar('Getting images', min=1, max=images.count(), suffix='%(index)d/%(max)d (%(percent)d%%) ETA: %(eta_td)s')
        for img in images:
            img.url_to_img()
            bar.next()
        bar.finish()
