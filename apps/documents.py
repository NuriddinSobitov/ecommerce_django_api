from django_elasticsearch_dsl import Document, Index, fields, CompletionField
from django_elasticsearch_dsl_drf.compat import StringField

from apps.models import Product

INDEX = Index('product')

INDEX.settings(number_of_shards=1, number_of_replicas=1)


@INDEX.doc_type
class ProductDocument(Document):
    id = fields.IntegerField(attr='id')

    title = StringField(
        fields={
            'raw': StringField(analyzer='keyword'),
            'suggest': CompletionField(),
        }
    )

    description = StringField(
        fields={
            'raw': StringField(analyzer='keyword'),
            'suggest': CompletionField(),
        }
    )

    class Django:
        model = Product