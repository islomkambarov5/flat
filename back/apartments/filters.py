# filters.py
import django_filters
from .models import Flat


class ApartmentFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')
    price_per_person_min = django_filters.NumberFilter(field_name='price_per_person', lookup_expr='gte')
    price_per_person_max = django_filters.NumberFilter(field_name='price_per_person', lookup_expr='lte')
    room_count = django_filters.NumberFilter(field_name='room_count')
    room_count_min = django_filters.NumberFilter(field_name='room_count', lookup_expr='gte')
    room_count_max = django_filters.NumberFilter(field_name='room_count', lookup_expr='lte')
    has_wifi = django_filters.BooleanFilter(field_name='has_wifi')
    has_ac = django_filters.BooleanFilter(field_name='has_ac')
    has_contract = django_filters.BooleanFilter(field_name='has_contract')

    class Meta:
        model = Flat
        fields = [
            'city',
            'price_per_person_min',
            'price_per_person_max',
            'room_count',
            'room_count_min',
            'room_count_max',
            'has_wifi',
            'has_ac',
            'has_contract',
        ]