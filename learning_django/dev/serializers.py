from rest_framework import serializers

from .models import SalesMan, Products

class SalesManSerializers(serializers.ModelSerializer):

    class Meta:
        model = SalesMan
        fields = ('id', 'name', 'email', 'phone_no', 'address', 'created_at', 'updated_at')

class ProductsSerializers(serializers.ModelSerializer):

    agent_name = serializers.CharField(source='agent.name', read_only=True)
    agent_email = serializers.EmailField(source='agent.email', read_only=True)
    
    class Meta:
        model = Products
        fields = ('id', 'name', 'price_in_dollars', 'agent_name', 'agent_email', 'created_at', 'updated_at')
