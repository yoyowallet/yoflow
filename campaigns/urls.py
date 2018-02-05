from django.urls import path
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from campaigns import flows


@require_http_methods(['GET'])
def get(request, pk, **kwargs):
    from campaigns.models import Campaign
    return JsonResponse(Campaign.objects.get(pk=pk).json)


urlpatterns = [
    path('', flows.CampaignFlow().urls),
    path('<int:pk>/', get),
]
