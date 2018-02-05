from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField

from yoflow.models import FlowModel


class Campaign(FlowModel):
    DRAFT = 1
    PENDING = 2
    REJECTED = 3
    APPROVED = 4
    DELETED = 5
    STATES = (
        (DRAFT, 'draft'),
        (PENDING, 'pending'),
        (REJECTED, 'rejected'),
        (APPROVED, 'approved'),
        (DELETED, 'deleted'),
    )
    retailer = models.PositiveIntegerField(null=False)  # TODO FK
    type = models.PositiveIntegerField(null=False) # TODO FK
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # TODO not null
    name = models.CharField(max_length=256)  # TODO validate length in JS
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    json = JSONField(default=dict(), blank=True)
    state = models.IntegerField(choices=STATES, default=DRAFT)

    def __str__(self):
        return "Campaign {}".format(self.pk)
