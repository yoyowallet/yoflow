from django.contrib import admin

from example import models, flows, forms

from yoflow.admin import FlowAdmin, FlowInline


@admin.register(models.Parent)
class ParentAdmin(FlowAdmin):
    flow = flows.ParentFlow
    form = forms.ParentForm
    list_display = ('name', 'state')
    list_filter = ('state',)


@admin.register(models.Example)
class ExampleAdmin(FlowAdmin):
    flow = flows.ExampleFlow
    form = forms.ExampleForm
    list_display = ('name', 'state')
    list_filter = ('state',)
