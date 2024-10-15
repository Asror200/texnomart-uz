from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from product.serializers import AttributeValueSerializer, AttributeKeySerializer

from product.models import AttributeValue, AttributeKey


class AttributeValueListAPIView(ListAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    permission_classes = (AllowAny,)


class AttributeKeyListAPIView(ListAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer
    permission_classes = (AllowAny,)
