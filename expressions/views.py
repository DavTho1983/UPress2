from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np

from lxml import etree

from .serialisers import ExpressionSerializer
from .models import Expression


class ExpressionAPIView(APIView):

    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer

    def get(self, request):
        return Response({'data': request.data})

    def post(self, request):
        root = etree.XML(request.data['expression'])

        def evaluate_expression(root):
            numbers = []
            for child in root:
                if child.tag == "number":
                    num = int(child.text)
                    numbers.append(num)

                elif child.tag == "add":
                    _ = evaluate_expression(child)
                    numbers.append(np.sum(_))

                elif child.tag == "multiply":
                    _ = evaluate_expression(child)
                    numbers.append(np.prod(_))

                elif child.tag == "divide":
                    _ = evaluate_expression(child)

                    def divide_list(_):
                        x = _[0]
                        for i in range(1, len(_)):
                            x = x / _[i]
                        return x

                    numbers.append(divide_list(_))

                elif child.tag == "minus":
                    _ = evaluate_expression(child)

                    def minus_list(_):
                        x = _[0]
                        for i in range(1, len(_)):
                            x = x - _[i]
                        return x

                    numbers.append(minus_list(_))

                else:
                    numbers.extend(evaluate_expression(child))

            return numbers

        newresults = evaluate_expression(root)
        print("[NEW RESULTS]", newresults)

        def expression_to_string(root):
            expression = ""
            operator_mapping = {
                "add": " + ",
                "minus": " - ",
                "divide": " / ",
                "multiply": " * "
            }
            for child in root:
                if child.tag != "root" and child.tag != "expression":
                    if child.tag == "number":
                        num = int(child.text)
                        if child != root[-1]:
                            expression += f"{num} {operator_mapping[root.tag]} "
                        else:
                            expression += f"{num}"

                    else:
                        if child != root[-1]:
                            expression += f"({expression_to_string(child)}) {operator_mapping[root.tag]} "
                        else:
                            expression += f"({expression_to_string(child)})"
                else:
                    expression += f"{expression_to_string(child)}"

            return expression

        newresults = expression_to_string(root)
        print("[NEW RESULTS]", newresults)
        return Response({'data': request.data})


class ExpressionAPIListView(generics.ListAPIView):
    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer


class ExpressionsAPIID(generics.RetrieveAPIView):
    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer