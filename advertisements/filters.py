
from django_filters import rest_framework as filters, DateFromToRangeFilter
from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    # TODO: задайте требуемые фильтры 'favorites',

    created_at = DateFromToRangeFilter()
        
    # status = filters.CharFilter(field_name='status',
    #                             lookup_expr='iexact')
    
    class Meta:
        model = Advertisement
        fields = ['id', 'status', 'created_at', 'creator', ]
        

