from rest_framework import serializers
from .models import ContractState, Contract, Qualification
from users_system.models import Organizer, Musician
from locations.models import District
import social_media_system.notifier


class ContractStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractState
        fields = ('id', 'state')


class ContractSerializer(serializers.ModelSerializer):
    district_id = serializers.IntegerField(write_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    organizer_name = serializers.CharField(source='organizer.first_name', read_only=True)
    musician_name = serializers.CharField(source='musician.first_name', read_only=True)
    state = serializers.CharField(source='contract_state.state', read_only=True)

    def create(self, validated_data):
        organizer = Organizer.objects.get(user=validated_data["organizer_id"])
        validated_data["organizer"] = organizer
        musician = Musician.objects.get(user=validated_data["musician_id"])
        validated_data["musician"] = musician
        district = District.objects.get(id=validated_data["district_id"])
        validated_data["district"] = district
        contract_state = ContractState.objects.get(state='unanswered')
        validated_data["contract_state"] = contract_state
        contract = Contract.objects.create(**validated_data)
        social_media_system.notifier.notifier(contract)
        return contract

    class Meta:
        model = Contract
        fields = ('id', 'name', 'address', 'reference',
                  'description', 'amount', 'start_date', 'end_date',
                  'district_name', 'organizer_name', 'musician_name', 'state', 'district_id')


class QualificationSerializer(serializers.ModelSerializer):
    contract_name = serializers.CharField(source='contract.name', read_only=True)

    def create(self, validated_data):
        contract = Contract.objects.get(id=validated_data["contract_id"])
        validated_data["contract"] = contract
        qualification = Qualification.objects.create(**validated_data)
        return qualification

    class Meta:
        model = Qualification
        fields = ('id', 'text', 'score', 'contract_name')
