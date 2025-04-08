from django.http import HttpResponse
from django.views import View
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from example import flows, models, serializers
from yoflow.decorators import transition


# django function based view example
def approved_function_view(request, pk):
    obj = models.Post.objects.get(pk=pk)
    flow = flows.PostFlow()
    flow.check_permissions(obj=obj, to_state=models.Post.APPROVED)
    flow.process(obj=obj, to_state=models.Post.APPROVED, request=request, meta=request.POST)
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# django class based view example
class ApprovedClassBasedView(View):
    flow = flows.PostFlow

    def get_object(self):
        return models.Post.objects.get(pk=self.kwargs["pk"])

    @transition(to_state=models.Post.APPROVED)
    def post(self, request, pk):
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# djangorestframework example
class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    flow = flows.PostFlow

    @action(methods=["post"], detail=True)
    @transition(to_state=models.Post.APPROVED)
    def approved(self, request, pk=None):
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=True)
    def history(self, request, pk=None):
        qs = self.get_object().yoflow_history.all()
        return Response(qs.values("created_at", "new_state", "previous_state", "meta", "user"))
