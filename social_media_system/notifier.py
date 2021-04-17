from contract_system.models import Contract
from social_media_system.models import Notification, Comment, Following


def notifier(object_observer):
    notification = None

    if isinstance(object_observer, Comment):
        notification = Notification(message=f'{object_observer.commenter.first_name} has commented your publication',
                                    profile=object_observer.publication.musician)
    if isinstance(object_observer, Following):
        notification = Notification(message=f'{object_observer.follower.first_name} has started to follow you',
                                    profile=object_observer.followed)
    if isinstance(object_observer, Contract):
        if object_observer.contract_state.state == 'unanswered':
            notification = Notification(message=f'{object_observer.organizer.first_name} has request you for a contract',
                                        profile=object_observer.musician)
        elif object_observer.contract_state.state == 'progress':
            notification = Notification(message=f'{object_observer.musician.first_name} has accepted the contract',
                                        profile=object_observer.organizer)
        elif object_observer.contract_state.state == 'cancelled':
            notification = Notification(message=f'{object_observer.musician.first_name} has cancelled the contract',
                                        profile=object_observer.organizer)
    notification.save()
    return None
