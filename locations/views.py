from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.views import *
from .serializers import RegionSerializer, ProvinceSerializer, DistrictSerializer
from .models import Region, Province, District


regions_response = openapi.Response('regions description', RegionSerializer(many=True))
provinces_response = openapi.Response('provinces description', ProvinceSerializer(many=True))
districts_response = openapi.Response('districts description', DistrictSerializer(many=True))


@swagger_auto_schema(method='get', responses={200: regions_response})
@api_view(['GET'])
def regions_list(request):
    if request.method == 'GET':
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: provinces_response})
@api_view(['GET'])
def list_provinces_by_region(request, region_id):
    if request.method == 'GET':
        provinces = Province.objects.filter(regionid=region_id)
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: districts_response})
@api_view(['GET'])
def list_districts_by_province(request, province_id):
    if request.method == 'GET':
        districts = District.objects.filter(provinceid=province_id)
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)