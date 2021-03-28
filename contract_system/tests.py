import json
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from locations.models import Region, Province, District
from users_system.models import User, Musician, Organizer
from .models import ContractState, Contract
from .serializers import ContractStateSerializer, ContractSerializer


class ContractStateTest(APITestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.unanswered = ContractState.objects.create(state='unanswered')
        self.in_progress = ContractState.objects.create(state='in progress')
        self.finalized = ContractState.objects.create(state='finalized')
        self.cancelled = ContractState.objects.create(state='cancelled')

    def test_get_all_contract_states(self):
        response = self.client.get(reverse('contract_state_list'))
        contract_states = ContractState.objects.all()
        serializer = ContractStateSerializer(contract_states, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ContractTest(APITestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.unanswered = ContractState.objects.get(state='unanswered')
        self.in_progress = ContractState.objects.get(state='progress')
        self.finalized = ContractState.objects.get(state='finalized')
        self.cancelled = ContractState.objects.get(state='cancelled')
        self.region_lima = Region.objects.create(name='Lima')
        self.province_lima = Province.objects.create(name='Lima', region=self.region_lima)
        self.los_olivos = District.objects.create(name='Los olivos', province=self.province_lima)
        self.mario = User.objects.create(email='magotor1304@gmail.com', password=make_password('pacheco98'))
        self.cesar = User.objects.create(email='cesar98@gmail.com', password=make_password('cesar98'))
        self.mario_musician = Musician.objects.create(first_name='mario', last_name='tataje', birth_date='13/04/2000',
                                                      phone='995995408', type='Musician', user=self.mario,
                                                      district=self.los_olivos)
        self.cesar_organizer = Organizer.objects.create(first_name='cesar', last_name='ramirez',
                                                        birth_date='21/03/1996',
                                                        phone='927528321', type='Organizer', user=self.cesar,
                                                        district=self.los_olivos)
        self.contract_one = Contract.objects.create(name='contract one', address='tokyo', reference='chiba',
                                                    start_date='7/10/2020', end_date='8/10/2020',
                                                    district=self.los_olivos, organizer=self.cesar_organizer,
                                                    musician=self.mario_musician, contract_state=self.unanswered)
        self.contract_two = Contract.objects.create(name='contract two', address='naples', reference='roma',
                                                    start_date='9/10/2020', end_date='10/10/2020',
                                                    district=self.los_olivos, organizer=self.cesar_organizer,
                                                    musician=self.mario_musician, contract_state=self.unanswered)
        self.valid_contract = {
            'name': 'contract three',
            'address': 'naples',
            'reference': 'sardinia',
            'start_date': '7/10/2020',
            'end_date': '8/10/2020',
            'district_id': self.los_olivos.id
        }
        self.invalid_contract = {
            'name': 'contract three',
            'address': '',
            'reference': 'sardinia',
            'start_date': '7/10/2020',
            'end_date': '8/10/2020',
            'district_id': self.los_olivos.id
        }

    def test_get_all_contract(self):
        response = self.client.get(reverse('contract_list'))
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_contracts_by_organizer(self):
        response = self.client.get(reverse('list_contracts_by_organizer',
                                           kwargs={'organizer_id': self.cesar_organizer.id}))
        contracts = Contract.objects.filter(organizer__id=self.cesar_organizer.id)
        serializer = ContractSerializer(contracts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_contracts_by_musician(self):
        response = self.client.get(reverse('list_contracts_by_musician',
                                           kwargs={'musician_id': self.mario_musician.id}))
        contracts = Contract.objects.filter(musician__id=self.mario_musician.id)
        serializer = ContractSerializer(contracts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_contract(self):
        response = self.client.get(reverse('contract_detail', kwargs={'contract_id': self.contract_one.id}))
        contract = Contract.objects.get(id=self.contract_one.id)
        serializer = ContractSerializer(contract)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_contract(self):
        response = self.client.get(reverse('contract_detail', kwargs={'contract_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_contract(self):
        response = self.client.post(
            reverse('create_contracts', kwargs={'organizer_id': self.cesar_organizer.id,
                                                'musician_id': self.mario_musician.id}),
            data=json.dumps(self.valid_contract),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_contract(self):
        response = self.client.post(
            reverse('create_contracts', kwargs={'organizer_id': self.cesar_organizer.id,
                                                'musician_id': self.mario_musician.id}),
            data=json.dumps(self.invalid_contract),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_contract(self):
        response = self.client.put(
            reverse('contract_detail', kwargs={'contract_id': self.contract_one.id}),
            data=json.dumps(self.valid_contract),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_contract(self):
        response = self.client.put(
            reverse('contract_detail', kwargs={'contract_id': self.contract_one.id}),
            data=json.dumps(self.invalid_contract),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_contract(self):
        response = self.client.delete(
            reverse('contract_detail', kwargs={'contract_id': self.contract_one.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_contract(self):
        response = self.client.delete(
            reverse('contract_detail', kwargs={'contract_id': 14}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_valid_contract_state(self):
        response = self.client.patch(
            reverse('update_contract_state', kwargs={'contract_id': self.contract_one.id,
                                                     'state_id': self.in_progress.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_invalid_contract_state(self):
        response = self.client.patch(
            reverse('update_contract_state', kwargs={'contract_id': self.contract_one.id,
                                                     'state_id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
