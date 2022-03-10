from rest_framework.generics import CreateAPIView
from tecnico.serializers.tecnico import TecnicoSerializer

class TecnicoAPIView(CreateAPIView):
    serializer_class = TecnicoSerializer

    
