from django.contrib import admin

from example import flows, models
from yoflow.admin import FlowAdmin


@admin.register(models.Post)
class ParentAdmin(FlowAdmin):
    flow = flows.PostFlow
    list_display = ('name', 'state')
    list_filter = ('state',)
