from agrotoxico.models import Agrotoxico
from agrotoxico.serializers.espera import EsperaSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class AgrotoxicoEsperaDetailAPIView(APIView):
    serializer_class = EsperaSerializer

    def get_object(self, pk):
        return get_object_or_404(Agrotoxico, pk=pk)

    def post(self, request, pk=None):
        agrotoxico = self.get_object(pk)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(agrotoxico=agrotoxico)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
