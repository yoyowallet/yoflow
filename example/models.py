from __future__ import unicode_literals

import uuid

from django.db import models

from yoflow.models import FlowModel


DRAFT = 1
APPROVED = 2
FINAL = 3
STATES = (
    (DRAFT, 'draft'),
    (APPROVED, 'approved'),
    (FINAL, 'final'),
)


class Parent(FlowModel):
    name = models.CharField(max_length=256, null=True, blank=True)
    state = models.IntegerField(choices=STATES, default=DRAFT)

    def __str__(self):
        return '{}'.format(self.name)


class Child(FlowModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    custom_state_field = models.IntegerField(choices=STATES, default=DRAFT)

    def __str__(self):
        return '{}'.format(self.name)
