from django.db import models

from yoflow.models import FlowModel


class Post(FlowModel):
    DRAFT = 1
    APPROVED = 2
    STATES = (
        (DRAFT, 'draft'),
        (APPROVED, 'approved'),
    )
    name = models.CharField(max_length=256)
    content = models.TextField()
    state = models.IntegerField(choices=STATES, default=DRAFT)
