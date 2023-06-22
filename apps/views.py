from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import SuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.documents import ProductDocument

from apps.models import Product, ProductImage, Category, Favourite
from apps.serializers import CategoryModelSerializer, CreateProductModelSerializer, ListProductModelSerializer, \
    ProductDocumentSerializer

images_params = openapi.Parameter('images', openapi.IN_FORM, description="test manual param", type=openapi.TYPE_ARRAY,
                                  items=openapi.Items(type=openapi.TYPE_FILE), required=True)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ListProductModelSerializer
    parser_classes = MultiPartParser, FormParser
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('title', 'brand', 'description')
    # filterset_class = CustomProductFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProductModelSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(tags=["products"], manual_parameters=[images_params])
    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            images_list = [ProductImage(image=image, product=product) for image in images]
            ProductImage.objects.bulk_create(images_list)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def favourite(self, request, pk=None):
        like = Favourite.objects.filter(product_id=pk, user=self.request.user).first()
        if like:
            like.delete()
        else:
            Favourite.objects.create(product_id=pk, user=self.request.user)
        return Response({'message': 'bajarildi'}, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        data = self.get_serializer(instance).data
        return Response(data)


class CategoryAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

# [{ "SSD": "512", "RAM": "16" }]


class ProductDocumentView(DocumentViewSet):
    document = ProductDocument
    serializer_class = ProductDocumentSerializer

    filter_backends = [
        SuggesterFilterBackend
    ]

    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }