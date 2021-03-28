from django.urls import path
from .views import regions_list, list_provinces_by_region, list_districts_by_province


urlpatterns = [
    path('regions/', regions_list, name='regions_list'),
    path('regions/<int:region_id>/provinces/', list_provinces_by_region, name='list_provinces_by_region'),
    path('provinces/<int:province_id>/districts/', list_districts_by_province, name='list_districts_by_province'),
]