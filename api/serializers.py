from rest_framework import serializers
from crm.models import Lead, Topic, About

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'user', 'name']
        read_only_fields = ['id', 'user']

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['body']

class LeadSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = Lead
        fields = ['id', 'user', 'topic', 'topic_name', 'name', 'email', 'phone', 'description']
        read_only_fields = ['id', 'user', 'topic_name']

    def validate_topic(self, value):
        user = self.context['request'].user
        if not user.topic_set.filter(pk=value.pk).exists():
            raise serializers.ValidationError("You can only select topics that you have.")
        return value