from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models


class Flow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    previous_state = models.CharField(
        max_length=getattr(settings, 'YOFLOW_STATE_MAX_LENGTH', 256), null=True
    )
    new_state = models.CharField(
        max_length=getattr(settings, 'YOFLOW_STATE_MAX_LENGTH', 256)
    )
    meta = JSONField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(
        max_length=getattr(settings, 'YOFLOW_OBJECT_ID_MAX_LENGTH', 256)
    )
    content_object = GenericForeignKey()

    def __str__(self):
        return '{} {}'.format(self.content_type, self.object_id)


class FlowModel(models.Model):
    yoflow_history = GenericRelation(Flow)

    class Meta:
        abstract = True
