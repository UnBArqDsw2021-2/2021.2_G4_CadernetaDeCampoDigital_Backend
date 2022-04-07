from core.consts.usuarios import TECNICO

from produtor.serializers.produtor import ProdutorSerializer

from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404

from tecnico.serializers.tecnico import TecnicoSerializer

from usuario.models import Usuario


class UsuarioRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    def get_object(self):
        usuario = get_object_or_404(Usuario, **self.kwargs)
        if usuario.tipo == TECNICO:
            return usuario.tecnico
        return usuario.produtor

    def get_serializer_class(self):
        if self.get_object().usuario.tipo == TECNICO:
            return TecnicoSerializer
        return ProdutorSerializer
