#-*- coding: utf-8 -*-
from django.db import models

class PGNfile(models.Model):
    player = models.CharField(max_length=255)
    pgnfile = models.FileField(upload_to='stats', max_length=255)

    def __unicode__(self):
        return self.pgnfile
