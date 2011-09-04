#-*- coding: utf-8 -*-
from django.db import models

class PGNfile(models.Model):

    pgnfile = models.FileField(upload_to="pgnfiles")
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.pgnfile

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.pgnfile.name
        super(PGNfile, self).save(*args, **kwargs)

