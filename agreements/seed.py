from agreements.models import ContractState, ReservationState


def create_data(apps, schema_editor):
    contract_states = ['unanswered', 'progress', 'cancelled', 'finalized']
    for contract_state in contract_states:
        ContractState(state=contract_state).save()


def create_data_reservations(apps, schema_editor):
    reservation_states = ['unanswered', 'rejected', 'accepted']
    for reservation_state in reservation_states:
        ReservationState(state=reservation_state).save()
