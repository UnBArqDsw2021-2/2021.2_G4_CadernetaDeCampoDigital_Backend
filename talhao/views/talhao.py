from rest_framework.generics import CreateAPIView, RetrieveAPIView

from talhao.models import Talhao
from talhao.serializers.talhao import TalhaoSerializer, TalhaoDetailSerializer


class TalhaoAPIView(CreateAPIView):
    serializer_class = TalhaoSerializer

    def get_queryset(self):
        return Talhao.objects.all()


class TalhaoDetailAPIView(RetrieveAPIView):
    serializer_class = TalhaoDetailSerializer
    lookup_field = 'idTalhao'

    def get_queryset(self):
        return Talhao.objects.all()
