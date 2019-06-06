from django.urls import path

from .views import ExpressionAPIView, ExpressionAPIListView, ExpressionsAPIID

urlpatterns = [
    path("", ExpressionAPIView.as_view(), name="post"),
    path("<int:pk>", ExpressionsAPIID.as_view(), name="detail"),
    path("list", ExpressionAPIListView.as_view(), name="list"),
]
