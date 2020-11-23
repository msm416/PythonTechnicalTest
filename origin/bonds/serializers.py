

from rest_framework import serializers

from bonds.models import Bond


class BondSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bond
        fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']

    def create(self, validated_data):
        bond = Bond.objects.create(**validated_data)
        return bond
