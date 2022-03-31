from agrotoxico.models import Espera

from rest_framework import serializers


class EsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espera
        fields = ('agrotoxico', 'cultura', 'diasCarencia')
        read_only_fields = ('agrotoxico',)

    def validate_cultura(self, cultura):
        agrotoxico = self.context["agrotoxico"]

        if agrotoxico.espera.filter(cultura=cultura).exists():
            raise serializers.ValidationError("Cultura já relacionada com o agrotóxico.")

        return cultura
