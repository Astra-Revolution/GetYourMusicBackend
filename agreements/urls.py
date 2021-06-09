from django.urls import path

from .views import contracts_state_list, reservations_state_list, event_list, events_organizer, event_detail,\
    reservation_list, list_contracts_by_organizer, list_contracts_by_musician, create_contracts, contract_detail,\
    update_contract_state, list_qualifications_by_musician, create_qualifications, qualification_detail

urlpatterns = [
    path('contractStates/', contracts_state_list, name='contract_state_list'),
    path('reservationStates/', reservations_state_list, name='reservation_state_list'),
    path('events/', event_list, name='event_list'),
    path('organizers/<int:organizer_id>/events/', events_organizer, name='events_organizer'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('musicians/<int:musician_id>/reservations/', reservation_list, name='reservation_list'),
    path('organizer-contracts/', list_contracts_by_organizer, name='list_contracts_by_organizer'),
    path('musician-contracts/', list_contracts_by_musician, name='list_contracts_by_musician'),
    path('organizers/<int:organizer_id>/musicians/<int:musician_id>/contracts/',
         create_contracts, name='create_contracts'),
    path('contracts/<int:contract_id>/', contract_detail, name='contract_detail'),
    path('contracts/<int:contract_id>/contract_states/<int:state_id>/', update_contract_state,
         name='update_contract_state'),
    path('musicians/<int:musician_id>/qualifications/', list_qualifications_by_musician,
         name='list_qualifications_by_musician'),
    path('contracts/<int:contract_id>/qualifications/', create_qualifications, name='create_qualifications'),
    path('qualifications/<int:qualification_id>/', qualification_detail, name='qualification_detail'),
]
