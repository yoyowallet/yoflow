from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from yoflow import forms, models


class FlowInline(GenericTabularInline):
    model = models.Flow
    extra = 0
    exclude = ('content_type',)
    readonly_fields = ('user', 'created_at', 'previous_state', 'new_state', 'meta')
    can_delete = False

    def has_add_permission(self, request):
        return False

class FlowAdmin(admin.ModelAdmin):

    form = forms.FlowForm

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.flow = self.flow()
        form.request = request
        return form

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(FlowAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [FlowInline]
        return super(FlowAdmin, self).change_view(request, object_id, form_url, extra_context)
