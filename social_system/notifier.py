from users_system.models import Following
from contract_system.models import Contract
from social_system.models import Notification, Comment


def notifier(Object, state=0):
    notification = None

    if isinstance(Object, Comment):
        notification = Notification(message=f'{Object.commenter.first_name} has commented your publication',
                                    profile=Object.publication.musician)
    if isinstance(Object, Following):
        notification = Notification(message=f'{Object.follower.first_name} has started to follow you',
                                    profile=Object.followed)
    if isinstance(Object, Contract):
        if state == 1:  # the organizer requests a musician for a contract
            notification = Notification(message=f'{Object.organizer.first_name} has request you for a contract',
                                        profile=Object.musician)
        elif state == 2:  # the musician acceptsin progress the contract
            if Object.contract_state.state == '':
                notification = Notification(message=f'{Object.musician.first_name} has accepted the contract',
                                            profile=Object.organizer)
            elif Object.contract_state.state == 'cancelled':
                notification = Notification(message=f'{Object.musician.first_name} has cancelled the contract',
                                            profile=Object.organizer)
    notification.save()
    return None
