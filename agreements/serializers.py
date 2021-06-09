from rest_framework import serializers

import social_media.notifier
from .models import ContractState, ReservationState, Event, Reservation, Contract, Qualification
from .utils import update_score_musician


class ContractStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractState
        fields = ('id', 'state')


class ReservationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationState
        fields = ('id', 'state')


class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.SerializerMethodField('get_organizer_full_name', read_only=True)
    organizer_image = serializers.CharField(source='organizer.image_url', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    @staticmethod
    def get_organizer_full_name(self):
        organizer = self.organizer
        full_name = f'{organizer.first_name} {organizer.last_name}'
        return full_name

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    class Meta:
        model = Event
        fields = ('id', 'name', 'address', 'reference', 'description', 'amount', 'start_date', 'end_date',
                  'district_name', 'organizer_name', 'organizer_image')


class ReservationSerializer(serializers.ModelSerializer):
    musician_name = serializers.SerializerMethodField('get_musician_full_name', read_only=True)
    musician_image = serializers.CharField(source='musician.image_url', read_only=True)

    @staticmethod
    def get_musician_full_name(self):
        musician = self.musician
        full_name = f'{musician.first_name} {musician.last_name}'
        return full_name

    def create(self, validated_data):
        reservation_state = ReservationState.objects.get(state='unanswered')
        validated_data["state"] = reservation_state
        return Event.objects.create(**validated_data)

    class Meta:
        model = Reservation
        fields = ('id', 'suggestion', 'date')


class ContractSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='event.name', read_only=True)
    address = serializers.CharField(source='event.address', read_only=True)
    reference = serializers.CharField(source='event.reference', read_only=True)
    description = serializers.CharField(source='event.description', read_only=True)
    amount = serializers.FloatField(source='event.amount', read_only=True)
    start_date = serializers.CharField(source='event.start_date', read_only=True)
    end_date = serializers.CharField(source='event.end_date', read_only=True)
    organizer_image = serializers.CharField(source='event.organizer.image_url', read_only=True)
    musician_image = serializers.CharField(source='musician.image_url', read_only=True)
    district_name = serializers.CharField(source='event.district.name', read_only=True)
    organizer_name = serializers.SerializerMethodField('get_organizer_full_name', read_only=True)
    musician_name = serializers.SerializerMethodField('get_musician_full_name', read_only=True)
    state = serializers.CharField(source='contract_state.state', read_only=True)

    @staticmethod
    def get_musician_full_name(self):
        musician = self.musician
        full_name = f'{musician.first_name} {musician.last_name}'
        return full_name

    @staticmethod
    def get_organizer_full_name(self):
        organizer = self.event.organizer
        full_name = f'{organizer.first_name} {organizer.last_name}'
        return full_name

    def create(self, validated_data):
        contract_state = ContractState.objects.get(state='unanswered')
        validated_data["contract_state"] = contract_state
        contract = Contract.objects.create(**validated_data)
        social_media.notifier.notifier(contract)
        return contract

    class Meta:
        model = Contract
        fields = ('id', 'name', 'address', 'reference', 'description', 'amount', 'start_date', 'end_date',
                  'district_name', 'organizer_name', 'musician_name', 'organizer_image', 'musician_image', 'state')


class QualificationSerializer(serializers.ModelSerializer):
    contract_name = serializers.CharField(source='contract.event.name', read_only=True)
    organizer_name = serializers.SerializerMethodField('get_organizer_full_name', read_only=True)

    @staticmethod
    def get_organizer_full_name(self):
        organizer = self.contract.event.organizer
        full_name = f'{organizer.first_name} {organizer.last_name}'
        return full_name

    def create(self, validated_data):
        qualification = Qualification.objects.create(**validated_data)
        update_score_musician(qualification)
        return qualification

    class Meta:
        model = Qualification
        fields = ('id', 'text', 'score', 'contract_name', 'organizer_name')
