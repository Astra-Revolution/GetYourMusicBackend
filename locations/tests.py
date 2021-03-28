from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Region, Province, District
from .serializers import RegionSerializer, ProvinceSerializer, DistrictSerializer


class RegionTest(APITestCase):

    def setUp(self):
        self.lima = Region.objects.create(name='Lima')
        self.piura = Region.objects.create(name='Piura')
        self.puno = Region.objects.create(name='Puno')
        self.arequipa = Region.objects.create(name='Arequipa')

    def test_get_all_regions(self):
        response = self.client.get(reverse('regions_list'))
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProvinceTest(APITestCase):
    def setUp(self):
        self.region_lima = Region.objects.create(name='Lima')
        self.lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.canete = Province.objects.create(name='Cañete', region=self.region_lima)
        self.barranca = Province.objects.create(name='Barranca', region=self.region_lima)
        self.huaral = Province.objects.create(name='Huaral', region=self.region_lima)

    def test_get_all_provinces_by_region(self):
        response = self.client.get(reverse('list_provinces_by_region',
                                           kwargs={'region_id': self.region_lima.id}))
        provinces = Province.objects.filter(region__id=self.region_lima.id)
        serializer = ProvinceSerializer(provinces, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DistrictTest(APITestCase):
    def setUp(self):
        self.region_lima = Region.objects.create(name='Lima')
        self.province_lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.los_olivos = District.objects.create(name='Los olivos', province=self.province_lima)
        self.pueblo_libre = District.objects.create(name='Pueblo Libre', province=self.province_lima)
        self.san_miguel = District.objects.create(name='San Miguel', province=self.province_lima)
        self.cercado = District.objects.create(name='Cercado', province=self.province_lima)

    def test_get_all_districts_by_province(self):
        response = self.client.get(reverse('list_districts_by_province',
                                           kwargs={'province_id': self.province_lima.id}))
        districts = District.objects.filter(province__id=self.province_lima.id)
        serializer = DistrictSerializer(districts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
