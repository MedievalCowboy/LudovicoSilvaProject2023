from django.test import TestCase

from . import views.


class OrdenTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_orders = 10
        ESTADOS = ["Por_aprobar,Tramitado,Finalizado"]

        for order_id in range(number_of_order):
            Author.objects.create(
                num_orden=f' {author_id}',
                estado=ESTADOS[order_id//2],
            )
    #Prueba de entrada al url de ordenes
    def test_views_ordenes_getAll(self):
        response = self.client.get('workspace/ordenes/')
        self.assertEqual(response.status_code, 200)
    #Prueba acceso por nombre util para llamadas en plantillas
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('ordenes'))
        self.assertEqual(response.status_code, 200)
    #Prueba de uso correcto de plantilla en ordenes
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('ordenes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ordenes.html')

        