from rest_framework import serializers
from .models import Sentiment


class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentiment
        fields = ['id', 'text', 'label']
        extra_kwargs = {
            'text': {'write_only': True},
        }

    def create(self, validated_data):
        sentiment = Sentiment.objects.create(**validated_data)
        return sentiment