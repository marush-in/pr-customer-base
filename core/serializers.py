
from rest_framework import serializers
from .models import Customer, Profession, DataSheet, Document


class CustomerSerializer(serializers.ModelSerializer):
    number_professions = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'id', 'name', 'address', 'professions', 'data_sheet', 'is_active',
            'status_message', 'number_professions'
        )

    def get_number_professions(self, obj):
        return obj.number_professions()


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description')


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('id', 'description', 'historical_data')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_number', 'customer')
