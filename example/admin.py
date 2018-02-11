from django.contrib import admin

from example import models, flows

from yoflow.admin import FlowAdmin, FlowInline


@admin.register(models.Parent)
class ParentAdmin(FlowAdmin):
    flow = flows.ParentFlow
    list_display = ('name', 'state')
    list_filter = ('state',)


@admin.register(models.Child)
class ExampleAdmin(FlowAdmin):
    flow = flows.ChildFlow
    list_display = ('name', 'custom_state_field')
    readonly_fields = ('uuid',)
    list_filter = ('custom_state_field',)
