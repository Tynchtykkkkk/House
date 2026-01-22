from django_filters import FilterSet
from .models import Property, City
class PropertyFilterSet(FilterSet):
    class Meta:
        model = Property
        fields = {
            'city': ['exact'],
            'property_type': ['exact'],
            'property_stars': ['exact'],
        }


class CityFilterSet(FilterSet):

    class Meta:
        model = City
        fields = ['city_name']