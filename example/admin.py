from django.contrib import admin
from yoflow.admin import FlowAdmin

from example import models, flows


@admin.register(models.Post)
class ParentAdmin(FlowAdmin):
    flow = flows.PostFlow
    list_display = ('name', 'state')
    list_filter = ('state',)
