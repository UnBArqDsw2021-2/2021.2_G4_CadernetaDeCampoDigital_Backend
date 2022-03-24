from rest_framework.generics import CreateAPIView

from talhao.models import Talhao
from talhao.serializers.talhao import TalhaoSerializer


class TalhaoAPIView(CreateAPIView):
    serializer_class = TalhaoSerializer

    def get_queryset(self):
        return Talhao.objects.all()
