from agreements.models import ContractState


def create_data(app, schema_editor):
    states = ['unanswered', 'progress', 'cancelled', 'finalized']
    for state in states:
        ContractState(state=state).save()