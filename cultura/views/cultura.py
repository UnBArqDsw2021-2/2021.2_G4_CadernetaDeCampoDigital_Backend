from cultura.models import Cultura
from cultura.serializers.cultura import CulturaSerializer

from rest_framework.generics import CreateAPIView


class CulturaAPIView(CreateAPIView):
    serializer_class = CulturaSerializer

    def get_queryset(self):
        return Cultura.objects.all()
