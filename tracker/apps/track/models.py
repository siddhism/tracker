from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ImproperlyConfigured

class Track(models.Model):
    """
    Model for Track data of user.
    Each track location is stored in this table.
    """
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50)


    def save(self, **kwargs):
        """
        Validation checks on cords in location
        """
        cords = self.location
        if not len(cords.split(',')) == 2:
            reason = 'please supply co ordinates seperated by comma'
            raise ImproperlyConfigured(reason)

        points = cords.split(',')
        try:
            latitude = float(cords.split(',')[0].strip())
            longitude = float(cords.split(',')[1].strip())
        except ValueError as e:
            print e
            reason = 'please supply integer/float values for co ordinates seperated by comma'
            raise ImproperlyConfigured(reason)

        super(Track, self).save(**kwargs)

    class Meta:
        verbose_name = "Track"
        verbose_name_plural = "Tracks"
