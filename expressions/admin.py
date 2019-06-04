from django.contrib import admin
from .models import Expression


@admin.register(Expression)
class ExpressionAdmin(admin.ModelAdmin):
    list_display = (
        "expression",
    )
    ordering = ["id"]