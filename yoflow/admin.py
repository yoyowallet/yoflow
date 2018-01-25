from django.contrib import admin


class FlowAdmin(admin.ModelAdmin):

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.flow = self.flow()
        return form
