from django.contrib import admin

from campaigns import models, flows

from yoflow.admin import FlowAdmin, FlowInline


@admin.register(models.Campaign)
class CampaignAdmin(FlowAdmin):
    flow = flows.CampaignFlow
    list_display = ('pk', 'state',)
    list_filter = ('state',)
    raw_id_fields = ('owner',)
