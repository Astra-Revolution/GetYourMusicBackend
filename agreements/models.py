from django.db import models
from accounts.models import Organizer, Musician
from locations.models import District


class ReservationState(models.Model):
    state = models.CharField(max_length=60)

    def __str__(self):
        return self.state

    class Meta:
        db_table = 'reservation_states'


class Event(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    reference = models.CharField(max_length=60)
    start_date = models.CharField(max_length=60)
    end_date = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    amount = models.FloatField(null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'events'


class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    state = models.ForeignKey(ReservationState, on_delete=models.CASCADE)
    suggestion = models.TextField()
    date = models.CharField(max_length=60)

    class Meta:
        db_table = 'reservations'


class ContractState(models.Model):
    state = models.CharField(max_length=60)

    def __str__(self):
        return self.state

    class Meta:
        db_table = 'contract_states'


class Contract(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    contract_state = models.ForeignKey(ContractState, on_delete=models.CASCADE)

    class Meta:
        db_table = 'contracts'


class Qualification(models.Model):
    text = models.CharField(max_length=60)
    score = models.FloatField()
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="qualification")

    class Meta:
        db_table = 'qualifications'
