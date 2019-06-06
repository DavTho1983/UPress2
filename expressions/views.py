from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from lxml import etree

from .serialisers import ExpressionSerializer
from .models import Expression


class ExpressionAPIView(APIView):



    def __init__(self):
        self.operator_mapping = {
            "add": " + ",
            "minus": " - ",
            "divide": " / ",
            "multiply": " * "
        }
        self.queryset = Expression.objects.all()
        self.serializer_class = ExpressionSerializer


    def get(self, request):
        return Response({'data': request.data})

    def post(self, request):
        root = etree.XML(request.data['expression'])

        result = self.evaluate_expression(root)[0]

        exp_parsed = self.expression_to_string(root) + f" = {result}"

        serializer_data = {'expression': exp_parsed, 'result': result}

        serializer = self.serializer_class(
            data=serializer_data,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def expression_to_string(self, root):
        expression = ""

        for child in root:
            if child.tag != "root" and child.tag != "expression":
                if child.tag == "number":
                    num = int(child.text)
                    if child != root[-1]:
                        expression += f"{num} {self.operator_mapping[root.tag]} "
                    else:
                        expression += f"{num}"

                else:
                    if child != root[-1]:
                        expression += f"({self.expression_to_string(child)}) {self.operator_mapping[root.tag]} "
                    else:
                        expression += f"({self.expression_to_string(child)})"
            else:
                expression += f"{self.expression_to_string(child)}"

        return expression

    def evaluate_expression(self, root):
        numbers = []
        for child in root:
            if child.tag == "number":
                num = int(child.text)
                numbers.append(num)

            elif child.tag in ["add", "minus", "divide", "multiply"]:
                _ = self.evaluate_expression(child)

                def eval_sublist(_, operator):
                    x = _[0]
                    for i in range(1, len(_)):
                        x_str = f"{x}{operator}{_[i]}"
                        x = eval(x_str)
                    return x

                numbers.append(eval_sublist(_, self.operator_mapping[child.tag]))

            else:
                numbers.extend(self.evaluate_expression(child))

        return numbers


class ExpressionAPIListView(generics.ListAPIView):
    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer


class ExpressionsAPIID(generics.RetrieveAPIView):
    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer