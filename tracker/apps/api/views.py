from django.shortcuts import render
from django.contrib.auth.models import User

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

    def filter_queryset(self, request, queryset):
        start_value = request.query_params.get(self.start_lookup)
        end_value = request.query_params.get(self.end_lookup)
        queryset = self.filter(queryset, start_value, end_value)
        return queryset


# Create your views here.
class IndexView(DateTimeRangeFilter, APIView):
    """
    """
    allowed_methods = ['GET', 'POST', 'PUT']
    serializer_class = TrackSerializer

    def get(self, request, *args, **kwargs):
        queryset = Track.objects.all()
        user_id = request.query_params.get('user')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'reason': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(user=user)

        queryset = self.filter_queryset(request, queryset)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Accepts comma seperated values as API params and converts them to geos Point
        """
        from django.contrib.gis.geos import Point
        user_id = request.data.get('user')
        # if not User.objects.filter(id=user_id).exists():
        #     raise Exception

        cords = request.data.get('location')
        # TODO : put validation here
        x = int(cords.split(',')[0].strip())
        y = int(cords.split(',')[1].strip())
        location = Point(x, y, srid=4326)
        data = request.data.dict()
        data['location'] = location

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)