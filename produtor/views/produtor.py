from produtor.models import Produtor
from produtor.serializers.produtor import ProdutorSerializer

from rest_framework.generics import CreateAPIView


class ProdutorAPIView(CreateAPIView):
    serializer_class = ProdutorSerializer

    def get_queryset(self):
        return Produtor.objects.all()
