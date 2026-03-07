from django.contrib import admin
from apps.common.models import Page


admin.register(Page)
class PageAdmin(admin.ModelAdmin):

    list_display = (
        "url",
        "title"
    )
