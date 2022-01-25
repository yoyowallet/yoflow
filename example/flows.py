from django.core.mail import send_mail

from example import models
from yoflow import flow


class PostFlow(flow.Flow):
    model = models.Post
    transitions = {
        model.DRAFT: [model.APPROVED],
        model.APPROVED: [],
    }

    @staticmethod
    def validate(view):
        return getattr(view.request, 'data', view.request.POST)

    @staticmethod
    def draft_to_approved(obj, meta):
        pass

    @staticmethod
    def on_approved(obj, meta):
        send_mail(
            'Approved!',
            '{} was approved'.format(obj),
            'from@example.com',
            ['to@example.com'],
        )

    @staticmethod
    def all(obj, meta):
        pass
