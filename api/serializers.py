from rest_framework import serializers
from django.contrib.auth.models import User
from crm.models import Lead, Topic

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']

class LeadSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = Lead
        fields = ['id', 'user', 'name', 'topic', 'email', 'phone', 'description']

    def create(self, validated_data):
        # Exclude user from validated_data, as it should not be created
        validated_data.pop('user','topic', None)
        return super().create(validated_data)