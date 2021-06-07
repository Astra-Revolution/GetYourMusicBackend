from rest_framework import serializers
from .models import ContractState, Contract, Qualification
from accounts.models import Organizer, Musician
from locations.models import District
import social_media.notifier


class ContractStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractState
        fields = ('id', 'state')


class ContractSerializer(serializers.ModelSerializer):
    district_id = serializers.IntegerField(write_only=True)
    organizer_image = serializers.CharField(source='organizer.image_url', read_only=True)
    musician_image = serializers.CharField(source='musician.image_url', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
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
        organizer = self.organizer
        full_name = f'{organizer.first_name} {organizer.last_name}'
        return full_name

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
        social_media.notifier.notifier(contract)
        return contract

    class Meta:
        model = Contract
        fields = ('id', 'name', 'address', 'reference', 'description', 'amount', 'start_date', 'end_date',
                  'district_name', 'organizer_name', 'musician_name', 'organizer_image', 'musician_image', 'state',
                  'district_id')


def update_score_musician(qualification):
    musician = qualification.contract.musician
    qualifications = Qualification.objects \
        .filter(contract__in=Contract.objects.filter(musician__user=musician.user.id))
    result = 0
    for qualification in qualifications:
        result = result + qualification.score
    result = result/qualifications.count()
    musician.rating = result
    musician.save()


class QualificationSerializer(serializers.ModelSerializer):
    contract_name = serializers.CharField(source='contract.name', read_only=True)
    organizer_name = serializers.SerializerMethodField('get_organizer_full_name', read_only=True)

    @staticmethod
    def get_organizer_full_name(self):
        organizer = self.contract.organizer
        full_name = f'{organizer.first_name} {organizer.last_name}'
        return full_name

    def create(self, validated_data):
        contract = Contract.objects.get(id=validated_data["contract_id"])
        validated_data["contract"] = contract
        qualification = Qualification.objects.create(**validated_data)
        update_score_musician(qualification)
        return qualification

    class Meta:
        model = Qualification
        fields = ('id', 'text', 'score', 'contract_name', 'organizer_name')