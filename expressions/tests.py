from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import Expression
from .views import ExpressionAPIView
from lxml import etree


class ExpressionModelTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def create_expression(self, expression="1 + 2 = 3", result=3):
        return Expression.objects.create(expression=expression, result=result)

    def test_expression_creation(self):
        _ = self.create_expression()
        self.assertTrue(isinstance(_, Expression))
        self.assertEqual("1 + 2 = 3", _.expression)
        self.assertEqual(3, _.result)


class ExpressionViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.ExpAPIView = ExpressionAPIView()

    def create_expression(self, expression="1 + 2 = 3", result=3):
        return Expression.objects.create(expression=expression, result=result)

    def test_expression_to_string(self):
        xml = "<root><expression><minus><number>24</number><number>3</number></minus></expression></root>"
        root = etree.XML(xml)
        exp_to_string = self.ExpAPIView.expression_to_string(root)
        self.assertEqual(exp_to_string, "(24  -  3)")
