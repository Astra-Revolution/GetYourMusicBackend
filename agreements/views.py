from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from accounts.models import Organizer, Musician
from .models import ContractState, ReservationState, Contract, Qualification
from .serializers import ContractStateSerializer, ReservationStateSerializer,\
    ContractSerializer, QualificationSerializer
import social_media.notifier

contract_states_response = openapi.Response('contract states description', ContractStateSerializer(many=True))
reservation_states_response = openapi.Response('reservation states description', ReservationStateSerializer(many=True))
contracts_response = openapi.Response('contracts description', ContractSerializer(many=True))
contract_response = openapi.Response('contract description', ContractSerializer)
qualifications_response = openapi.Response('qualifications description', QualificationSerializer(many=True))
qualification_response = openapi.Response('qualifications description', QualificationSerializer)
organizer_param = openapi.Parameter('organizer_id', openapi.IN_QUERY, description="organizer id",
                                    type=openapi.TYPE_INTEGER)
musician_param = openapi.Parameter('musician_id', openapi.IN_QUERY, description="musician id",
                                   type=openapi.TYPE_INTEGER)
state_param = openapi.Parameter('state_id', openapi.IN_QUERY, description="state id", type=openapi.TYPE_INTEGER)


@swagger_auto_schema(method='get', responses={200: contract_states_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contracts_state_list(request):
    if request.method == 'GET':
        contract_states = ContractState.objects.all()
        serializer = ContractStateSerializer(contract_states, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: reservation_states_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reservations_state_list(request):
    if request.method == 'GET':
        reservation_states = ReservationState.objects.all()
        serializer = ReservationStateSerializer(reservation_states, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: contracts_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contract_list(request):
    if request.method == 'GET':
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: contracts_response},
                     manual_parameters=[organizer_param, state_param])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_contracts_by_organizer(request):
    if request.method == 'GET':
        organizer_id = int(request.query_params.get('organizer_id'))
        state_id = int(request.query_params.get('state_id'))
        contracts = Contract.objects.filter(organizer__user=organizer_id, contract_state__id=state_id)
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: contracts_response},
                     manual_parameters=[musician_param, state_param])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_contracts_by_musician(request):
    if request.method == 'GET':
        musician_id = int(request.query_params.get('musician_id'))
        state_id = int(request.query_params.get('state_id'))
        contracts = Contract.objects.filter(musician__user=musician_id, contract_state__id=state_id)
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=ContractSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_contracts(request, organizer_id, musician_id):
    if request.method == 'POST':
        try:
            Organizer.objects.get(user=organizer_id)
        except Organizer.DoesNotExist:
            raise Http404

        try:
            Musician.objects.get(user=musician_id)
        except Musician.DoesNotExist:
            raise Http404

        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer_id=organizer_id, musician_id=musician_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: contract_response})
@swagger_auto_schema(methods=['put'], request_body=ContractSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def contract_detail(request, contract_id):
    try:
        contract = Contract.objects.get(id=contract_id)
    except Contract.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = ContractSerializer(contract)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContractSerializer(contract, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contract.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(methods=['patch'], request_body=ContractSerializer)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_contract_state(request, contract_id, state_id):
    try:
        contract = Contract.objects.get(id=contract_id)
    except Contract.DoesNotExist:
        raise Http404

    try:
        state = ContractState.objects.get(id=state_id)
    except ContractState.DoesNotExist:
        raise Http404

    if request.method == 'PATCH':
        contract.contract_state = state
        social_media.notifier.notifier(contract)
        serializer = ContractSerializer(contract, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: qualifications_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_qualifications_by_musician(request, musician_id):
    if request.method == 'GET':
        # contracts = Contract.objects.filter(musician__id=musician_id)
        # qualifications = Qualification.objects.filter(contract__in=contracts)
        qualifications = Qualification.objects\
            .filter(contract__in=Contract.objects.filter(musician__user=musician_id))
        serializer = QualificationSerializer(qualifications, many=True)
        return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=QualificationSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_qualifications(request, contract_id):
    if request.method == 'POST':
        try:
            Contract.objects.get(id=contract_id)
        except Contract.DoesNotExist:
            raise Http404

        serializer = QualificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contract_id=contract_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: qualification_response})
@swagger_auto_schema(methods=['put'], request_body=QualificationSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def qualification_detail(request, qualification_id):
    try:
        qualification = Qualification.objects.get(id=qualification_id)
    except Qualification.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = QualificationSerializer(qualification)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QualificationSerializer(qualification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        qualification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
