from django.db import models
from users_system.models import Organizer, Musician
from locations.models import District


class ContractState(models.Model):
    state = models.CharField(max_length=60)

    def __str__(self):
        return self.state

    class Meta:
        db_table = 'contract_states'


class Contract(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    reference = models.CharField(max_length=60)
    start_date = models.CharField(max_length=60)
    end_date = models.CharField(max_length=60)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    contract_state = models.ForeignKey(ContractState, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'contracts'


class Qualification(models.Model):
    text = models.CharField(max_length=60)
    score = models.FloatField()
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="qualification")

    class Meta:
        db_table = 'qualifications'
