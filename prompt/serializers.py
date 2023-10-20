from rest_framework import serializers
from .models import Prompt

class PromptSerializer(serializers.ModelSerializer):

  class Meta:
      model = Prompt
      fields = ( 'User', 'gender', 'sensitivity_to_cold')

      def create(self, validated_data):
        return super(PromptSerializer, self).create(validated_data)