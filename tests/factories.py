import factory
import factory.fuzzy

from example import models


class DraftParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Parent
    name = factory.fuzzy.FuzzyText()
    state = models.DRAFT


class ApprovedParentFactory(DraftParentFactory):
    state = models.APPROVED


class FinalParentFactory(DraftParentFactory):
    state = models.FINAL