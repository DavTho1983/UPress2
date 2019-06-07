from rest_framework import serializers

from .models import Expression


class ExpressionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.operator_mapping = {"add": " + ", "minus": " - ", "divide": " / ", "multiply": " * "}
        super(ExpressionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Expression
        fields = ["expression", "result"]
        read_only_fields = ["result"]

    def create(self, validated_data):

        expression_obj = Expression.objects.create(**validated_data, result=self.initial_data["result"])

        return expression_obj

    def update(self, instance, validated_data):
        instance.expression = validated_data.get("expression", instance.expression)
        instance.result = self.context.get("result", instance.result)
        instance.save()
        return instance
