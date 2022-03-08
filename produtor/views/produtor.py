from produtor.models import Produtor
from produtor.serializers.produtor import ProdutorSerializer

from rest_framework.generics import ListCreateAPIView


class ProdutorAPIView(ListCreateAPIView):
    serializer_class = ProdutorSerializer

    def get_queryset(self):
        return Produtor.objects.all()
