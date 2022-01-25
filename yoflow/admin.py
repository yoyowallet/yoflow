from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.urls import reverse
from django.utils.html import format_html

from yoflow import forms, models


@admin.register(models.Flow)
class FlowMetaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content_type', 'previous_state', 'new_state')
    list_filter = ('content_type', 'created_at')
    readonly_fields = (
        'id',
        'user',
        'created_at',
        'previous_state',
        'new_state',
        'meta',
        'link',
    )
    exclude = ('content_type', 'object_id')

    def link(self, obj):
        app_label = obj.content_object._meta.app_label
        model_name = obj.content_object._meta.model_name
        url = reverse(
            'admin:{}_{}_change'.format(app_label, model_name), args=(obj.object_id,)
        )
        return format_html('<a href="{}">{}</a>'.format(url, obj.content_object))


class FlowInline(GenericTabularInline):
    model = models.Flow
    extra = 0
    exclude = (
        'content_type',
        'meta',
    )
    readonly_fields = (
        'link',
        'user',
        'created_at',
        'previous_state',
        'new_state',
    )
    ordering = ('-pk',)
    can_delete = False

    def link(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        url = reverse(
            'admin:{}_{}_change'.format(app_label, model_name), args=(obj.pk,)
        )
        return format_html('<a href="{}">{}</a>'.format(url, obj.pk))

    def has_add_permission(self, request):
        return False


class FlowAdmin(admin.ModelAdmin):

    form = forms.FlowForm

    def get_form(self, request, obj, **kwargs):
        form = super(FlowAdmin, self).get_form(request, obj, **kwargs)
        form.flow = self.flow()
        form.request = request
        return form

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(FlowAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [FlowInline]
        return super(FlowAdmin, self).change_view(
            request, object_id, form_url, extra_context
        )
