from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer, Profession, DataSheet, Document
from .serializers import(
    CustomerSerializer,
    ProfessionSerializer, 
    DataSheetSerializer,
    DocumentSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        active_customers = Customer.objects.filter(is_active=True)
        return active_customers

    def list(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        customer = self.get_object()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(
            name=data['name'],
            address=data['address'],
            data_sheet_id=data['data_sheet'],
        )
        profession = Profession.objects.get(id=data['professions'])
        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']
        profession = Profession.objects.get(id=data['professions'])

        for p in customer.professions.all():
            customer.professions.remove(p)

        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)

        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get('data_sheet', data_sheet_id.name)
        customer.save()

        serializer = CustomerSerializer(customer)

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()

        return Response('Object Removed.')
    
    @action(detail=True)
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.is_active = False
        customer.save()

        serializer = CustomerSerializer(customer)

        return Response(serializer.data)
    
    @action(detail=False)
    def deactivate_all(self, request, **kwargs):
        customers = Customer.objects.all()
        customers.update(is_active=False)

        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = Customer.objects.all()
        customers.update(is_active=True)

        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):
        status = True if request.data['is_active'] == True else False
        customers = Customer.objects.all()
        customers.update(is_active=status)

        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)


    

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer