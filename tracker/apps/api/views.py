from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.utils import timezone

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..track.models import Track
from .serializers import TrackSerializer

class DateTimeRangeFilter(object):
    """
    DateTime field specific filters
    supported filters:
        field__start : After this datetime
        field__end : Before this datetime
    """
    field_name = 'created_at'
    start_lookup = 'created_at__start'
    end_lookup = 'created_at__end'

    def filter(self, qs, start_value=None, stop_value=None):
        if start_value is not None and stop_value is not None:
            lookup = '%s__range' % self.field_name
            return qs.filter(**{lookup: (start_value, stop_value)})
        else:
            if start_value is not None:
                qs = qs.filter(**{'%s__gte' % self.field_name: start_value})
            if stop_value is not None:
                qs = qs.filter(**{'%s__lte' % self.field_name: stop_value})
        qs = qs.distinct()
        return qs


class IndexView(DateTimeRangeFilter, APIView):
    """
    Index view for API
    """
    allowed_methods = ['GET', 'POST', 'PUT']
    serializer_class = TrackSerializer

    def get_distance_covered(self, queryset):
        """
        Iterate over all points and sum up distance
        """
        distance = 0
        queryset = queryset.order_by('-created_at')
        starting_point = queryset.first()
        if not queryset.exists() or not starting_point:
            return distance
        for i in range(1, queryset.count()):
            source = queryset[i-1]
            destination = queryset[i]
            source_location = GEOSGeometry(source.location)
            destination_location = GEOSGeometry(destination.location)
            delta = source_location.distance(destination_location)
            distance = distance + delta
        return distance


    def get(self, request, *args, **kwargs):
        queryset = Track.objects.all()
        user_id = request.query_params.get('user')

        # If user id is provided return that particular user's data
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'reason': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(user=user)

        start_value = request.query_params.get(self.start_lookup)
        end_value = request.query_params.get(self.end_lookup)

        if start_value or end_value:
            queryset = self.filter(queryset, start_value, end_value)
        else:
            # If no date range is supplied we return data of today only
            start_value = timezone.now().replace(hour=0, minute=0, second=0)
            queryset = self.filter(queryset, start_value)

        distance = self.get_distance_covered(queryset)
        serializer = self.serializer_class(queryset, many=True)
        data = {'distance': distance, 'data': serializer.data}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Accepts comma seperated values as API params and converts them to geos Point
        """
        from django.contrib.gis.geos import Point
        user_id = request.data.get('user')

        cords = request.data.get('location')

        if not len(cords.split(',')) == 2:
            reason = 'please supply co ordinates seperated by comma'
            return Response({'reason': reason}, status=status.HTTP_400_BAD_REQUEST)

        x = float(cords.split(',')[0].strip())
        y = float(cords.split(',')[1].strip())
        location = Point(x, y, srid=4326)
        data = request.data.dict()
        data['location'] = location

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)