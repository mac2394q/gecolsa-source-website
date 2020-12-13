from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex

from cms.models import Communication
from cms.models import Page


class CommunicationIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', boost=1.125)

    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return Communication

    def get_updated_field(self):
        """Indicates which field can be used to filter objects by modification
        date"""
        return 'updated_at'

    def index_queryset(self, using=None):
        """Base queryset used to determine which objects to index.
        is used both when updating the index, and when creating it from scratch
        """
        return self.get_model().objects.filter(
            is_active=True,
        )


class PageIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', boost=1.125)

    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return Page

    def get_updated_field(self):
        """Indicates which field can be used to filter objects by modification
        date"""
        return 'updated_at'

    def index_queryset(self, using=None):
        """Base queryset used to determine which objects to index.
        is used both when updating the index, and when creating it from scratch
        """
        return self.get_model().objects.filter(
            is_active=True,
        )
