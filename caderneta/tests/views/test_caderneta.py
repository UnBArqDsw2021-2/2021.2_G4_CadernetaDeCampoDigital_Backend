from django.urls import reverse_lazy
from core.tests.mixin import APITestMixin
from django.test import TestCase
from plantio.tests.recipes import plantio as plantio_recipe, aplicacao as aplicacao_recipe


class CadernetaApiViewTest(APITestMixin, TestCase):
    def setUp(self):
        self.plantio = plantio_recipe.make()
        aplicacao_recipe.make(plantio=self.plantio)

    def get_url(self, idPlantio=None):
        if idPlantio is None:
            idPlantio = self.plantio.idPlantio
        return reverse_lazy('caderneta-detail', kwargs={"idPlantio": idPlantio})

    def test_detalha_caderneta(self):
        response = self.client.get(self.get_url())
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(data.keys()), {'idPlantio', 'dataPlantio', 'estado', 'cultura', 'talhao', 'aplicacoes'})
        self.assertEqual(set(data['cultura']), {'idCultura', 'nome', 'foto'})
        self.assertEqual(set(data['talhao']), {'idTalhao', 'numero', 'propriedade'})
        self.assertEqual(
            set(data['aplicacoes'][0]),
            {'idAplicacao', 'agrotoxico', 'dataAplicacao', 'fotoAgrotoxico', 'dosagemAplicacao', 'estadoAnalise', 'diasCarencia'}
        )
