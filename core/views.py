from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from rest_framework import viewsets
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
        customers = Customer.objects.filter(id=1)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     return HttpResponseNotAllowed('NOT ALLOWED.')

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

    
class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer