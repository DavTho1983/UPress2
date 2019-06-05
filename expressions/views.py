from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy as np

# from xml.etree import ElementTree
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

        def addleafnodes(root):
            numbers = []
            expression = ""
            for child in root:
                if child.tag == "number":
                    numbers.append(int(child.text))
                elif child.tag == "add":
                    _ = addleafnodes(child)
                    numbers.append(np.sum(_))
                    operator = " + "
                    _a = (operator.join(str(i) for i in _))
                    expression += f"({_a})"

                elif child.tag == "multiply":
                    _ = addleafnodes(child)
                    numbers.append(np.prod(_))
                    operator = " * "
                    _a = (operator.join(str(i) for i in _))
                    expression += f"({_a})"

                elif child.tag == "divide":
                    _ = addleafnodes(child)

                    def divide_list(_):
                        x = _[0]
                        for i in range(1, len(_)):
                            x = x / _[i]
                        return x

                    numbers.append(divide_list(_))
                    operator = " / "
                    _a = (operator.join(str(i) for i in _))
                    expression += f"({_a})"

                elif child.tag == "minus":
                    _ = addleafnodes(child)

                    def minus_list(_):
                        x = _[0]
                        for i in range(1, len(_)):
                            x = x - _[i]
                        return x

                    numbers.append(minus_list(_))
                    operator = " - "
                    _a = (operator.join(str(i) for i in _))
                    expression += f"({_a})"

                else:
                    numbers.extend(addleafnodes(child))

            print(expression)
            return numbers

        newresults = addleafnodes(root)
        print("[NEW RESULTS]", newresults)
        return Response({'data': request.data})


class ExpressionAPIListView(generics.ListAPIView):
    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer


class ExpressionsAPIID(generics.RetrieveAPIView):
    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer