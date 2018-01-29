from __future__ import unicode_literals

from django.db import models

from yoflow import permissions
from yoflow.models import FlowModel


DRAFT = 1
APPROVED = 2
STATES = (
    (DRAFT, 'draft'),
    (APPROVED, 'approved'),
)


class Parent(FlowModel):
    name = models.CharField(max_length=256, null=True, blank=True)
    state = models.IntegerField(choices=STATES, default=DRAFT)

    def __str__(self):
        return '{}'.format(self.name)


class Example(FlowModel):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    state = models.IntegerField(choices=STATES, default=DRAFT)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        permissions = permissions(STATES)
