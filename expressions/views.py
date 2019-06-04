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
            for child in root:
                if child.tag == "number":
                    numbers.append(int(child.text))
                elif child.tag == "add":
                    numbers.append(np.sum(addleafnodes(child)))
                elif child.tag == "multiply":
                    numbers.append(np.prod(addleafnodes(child)))
                elif child.tag == "divide":
                    to_divide = addleafnodes(child)

                    def divide_list(to_divide):
                        x = to_divide[0]
                        for i in range(1, len(to_divide)):
                            x = x / to_divide[i]
                        return x






                    numbers.append(divide_list(to_divide))



                else:
                    numbers.extend(addleafnodes(child))
                print("NUMBERS: ", numbers)
            return numbers

        newresults = addleafnodes(root)
        print("[NEW RESULTS]", newresults)

        # for sum in root.iter(tag=None):
        #     print(sum.tag, sum.attrib, sum.text)
        #
        # leaf_text = root.findall('.//number')
        # leaf_parent_tag = root.find('.//number/..')
        #
        # for x in range(0, len(leaf_text)):
        #     print(leaf_text[x].text, leaf_text[x].tag)
        #
        # for x in range(0, len(leaf_parent_tag)):
        #     print(leaf_parent_tag[x])
        return Response({'data': request.data})


class ExpressionAPIListView(generics.ListAPIView):
    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer


class ExpressionsAPIID(generics.RetrieveAPIView):
    queryset = Expression.objects.all()
    serializer_class = ExpressionSerializer