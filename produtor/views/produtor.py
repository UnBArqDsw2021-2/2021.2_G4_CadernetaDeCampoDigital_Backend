from produtor.models import Produtor
from produtor.serializers.produtor import ProdutorSerializer

from rest_framework.generics import ListCreateAPIView


class ProdutorAPIView(ListCreateAPIView):
    serializer_class = ProdutorSerializer
    queryset = Produtor.objects.all()
