from django.contrib import admin

from example import models, flows

from yoflow.admin import FlowAdmin, FlowInline


@admin.register(models.Parent)
class ParentAdmin(FlowAdmin):
    flow = flows.ParentFlow
    list_display = ('name', 'state')
    list_filter = ('state',)


@admin.register(models.Example)
class ExampleAdmin(FlowAdmin):
    flow = flows.ExampleFlow
    list_display = ('name', 'state')
    readonly_fields = ('uuid',)
    list_filter = ('state',)
