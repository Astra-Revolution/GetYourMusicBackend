from .models import Event, Contract, Qualification


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


def create_event(data, organizer, district):
    event = Event.objects.create(name=data['name'], address=data['address'], reference=data['reference'],
                                 description=data['description'], amount=data['amount'], start_date=data['start_date'],
                                 end_date=data['end_date'], organizer=organizer, district=district)
    return event
