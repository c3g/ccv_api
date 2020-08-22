from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .models.base import CanadianCommonCv
from .serializers import CanadianCommonCvSerializer


class CcvList(ListAPIView):
    queryset = CanadianCommonCv.objects.all()
    serializer_class = CanadianCommonCvSerializer
    pagination_class = PageNumberPagination
