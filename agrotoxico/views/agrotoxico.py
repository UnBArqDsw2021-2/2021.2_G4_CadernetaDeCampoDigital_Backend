from agrotoxico.models import Agrotoxico
from agrotoxico.serializers.agrotoxico import AgrotoxicoCreateSerializer, AgrotoxicoListSerializer

from cultura.models import Espera

from plantio.models import AplicacaoAgrotoxico

from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status


class AgrotoxicoAPIView(ListCreateAPIView):
    queryset = Agrotoxico.objects.all()

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return AgrotoxicoListSerializer
        return AgrotoxicoCreateSerializer


class AgrotoxicoDestroyAPIView(DestroyAPIView):
    queryset = Agrotoxico.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if AplicacaoAgrotoxico.objects.filter(agrotoxico=instance).exists():
            return Response(
                {'agrotoxico': 'Não é possível apagar um agrotoxico que já foi aplicado em um plantio.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Espera.objects.filter(agrotoxico=instance).exists():
            return Response(
                {'agrotoxico': 'Não é possível apagar um agrotoxico que está em tempo de espera de uma cultura.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
