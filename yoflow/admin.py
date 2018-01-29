from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from yoflow import models


class FlowInline(GenericTabularInline):
    model = models.Flow
    extra = 0
    exclude = ('content_type',)
    can_delete = False

    def get_fields(self, request, obj=None):
        fields = ('user', 'previous_state', 'new_state', 'meta')
        if obj:
            fields = fields + ('created_at',)
        return fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in self.model._meta.fields]
        return self.readonly_fields

    def has_add_permission(self, request):
        return False


class FlowAdmin(admin.ModelAdmin):

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
