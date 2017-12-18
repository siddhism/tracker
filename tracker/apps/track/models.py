from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Track(models.Model):
    """
    Model for Track data of user.
    Each track location is stored in this table.
    """
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.PointField(null=True, blank=True)

    objects = models.GeoManager()


    class Meta:
        verbose_name = "Track"
        verbose_name_plural = "Tracks"
