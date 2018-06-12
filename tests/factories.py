import factory
import factory.fuzzy

from example import models


class DraftPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post
    name = factory.fuzzy.FuzzyText()
    content = factory.fuzzy.FuzzyText()
    state = models.Post.DRAFT


class ApprovedPostFactory(DraftPostFactory):
    state = models.Post.APPROVED
