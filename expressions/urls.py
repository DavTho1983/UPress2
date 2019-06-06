from django.urls import path

from .views import ExpressionAPIView, ExpressionsAPIID

urlpatterns = [
    path("", ExpressionAPIView.as_view(), name="post"),
    path("<int:pk>", ExpressionsAPIID.as_view(), name="detail"),
]