from cultura.models import Cultura
from cultura.serializers.cultura import CulturaSerializer

from rest_framework.generics import ListCreateAPIView


class CulturaListCreateAPIView(ListCreateAPIView):
    serializer_class = CulturaSerializer

    def get_queryset(self):
        return Cultura.objects.all()
