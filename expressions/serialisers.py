from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Expression


class ExpressionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.operator_mapping = {
            "add": " + ",
            "minus": " - ",
            "divide": " / ",
            "multiply": " * "
        }
        super(ExpressionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Expression
        fields = ["expression"]

    def create(self, validated_data):

        expression_obj = Expression.objects.create(**validated_data)

        return expression_obj

