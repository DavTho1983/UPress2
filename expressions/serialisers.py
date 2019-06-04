from rest_framework import serializers
from .models import Expression


class ExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expression
        fields = "__all__"
