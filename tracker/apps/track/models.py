from __future__ import unicode_literals
import re

from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.forms import ValidationError

def validate_lat_long(value):
    regex = '^[-+]?([1-8]?\\d(\\.\\d+)?|90(\\.0+)?),\\s*[-+]?(180(\\.0+)?|((1[0-7]\\d)|([1-9]?\\d))(\\.\\d+)?)$'
    if not re.match(regex, value):
        raise ValidationError(
            '{} is not a valid location'.format(value)
        )

class Track(models.Model):
    """
    Model for Track data of user.
    Each track location is stored in this table.
    """
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50, validators=[validate_lat_long])


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
