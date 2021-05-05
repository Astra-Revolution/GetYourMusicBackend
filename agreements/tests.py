import json
from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from locations.models import Region, Province, District
from accounts.models import User, Musician, Organizer
from .models import ContractState, Contract, Qualification
from .serializers import ContractStateSerializer, ContractSerializer, QualificationSerializer


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
        response = self.client.get(reverse('list_contracts_by_organizer'),
                                   {'organizer_id': self.cesar_organizer.user.id,
                                    'state_id': self.unanswered.id})
        contracts = Contract.objects.filter(organizer__user=self.cesar_organizer.user.id)
        serializer = ContractSerializer(contracts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_contracts_by_musician(self):
        response = self.client.get(reverse('list_contracts_by_musician'),
                                   {'musician_id': self.mario_musician.user.id,
                                    'state_id': self.unanswered.id})
        contracts = Contract.objects.filter(musician__user=self.mario_musician.user.id)
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
            reverse('create_contracts', kwargs={'organizer_id': self.cesar_organizer.user.id,
                                                'musician_id': self.mario_musician.user.id}),
            data=json.dumps(self.valid_contract),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_contract(self):
        response = self.client.post(
            reverse('create_contracts', kwargs={'organizer_id': self.cesar_organizer.user.id,
                                                'musician_id': self.mario_musician.user.id}),
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


class QualificationTest(APITestCase):
    def setUp(self):
        admin = User.objects.create(email='admin@gmail.com', password=make_password('admin98'))
        self.client.force_authenticate(user=admin)
        self.finalized = ContractState.objects.create(state='finalized')
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
                                                    musician=self.mario_musician, contract_state=self.finalized)
        self.contract_two = Contract.objects.create(name='contract two', address='naples', reference='roma',
                                                    start_date='9/10/2020', end_date='10/10/2020',
                                                    district=self.los_olivos, organizer=self.cesar_organizer,
                                                    musician=self.mario_musician, contract_state=self.finalized)
        self.qualification = Qualification.objects.create(text='Hi, your very talented', score=4.4,
                                                          contract=self.contract_one)
        self.valid_qualification = {
            'text': 'Hi, test',
            'score': 3.8,
        }
        self.invalid_qualification = {
            'text': '',
            'score': 3.8,
        }

    def test_get_all_qualifications_by_musician(self):
        response = self.client.get(reverse('list_qualifications_by_musician',
                                           kwargs={'musician_id': self.mario_musician.user.id}))
        qualifications = Qualification.objects\
            .filter(contract__in=Contract.objects.filter(musician__user=self.mario_musician.user.id))
        serializer = QualificationSerializer(qualifications, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_qualification(self):
        response = self.client.get(reverse('qualification_detail',
                                           kwargs={'qualification_id': self.qualification.id}))
        qualification = Qualification.objects.get(id=self.qualification.id)
        serializer = QualificationSerializer(qualification)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_qualification(self):
        response = self.client.get(reverse('qualification_detail', kwargs={'qualification_id': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_qualification(self):
        response = self.client.post(
            reverse('create_qualifications', kwargs={'contract_id': self.contract_two.id}),
            data=json.dumps(self.valid_qualification),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_qualification(self):
        response = self.client.post(
            reverse('create_qualifications', kwargs={'contract_id': self.contract_two.id}),
            data=json.dumps(self.invalid_qualification),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_qualification(self):
        response = self.client.put(
            reverse('qualification_detail', kwargs={'qualification_id': self.qualification.id}),
            data=json.dumps(self.valid_qualification),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_qualification(self):
        response = self.client.put(
            reverse('qualification_detail', kwargs={'qualification_id': self.qualification.id}),
            data=json.dumps(self.invalid_qualification),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_qualification(self):
        response = self.client.delete(
            reverse('qualification_detail', kwargs={'qualification_id': self.qualification.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_qualification(self):
        response = self.client.delete(
            reverse('qualification_detail', kwargs={'qualification_id': 20}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
