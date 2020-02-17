from django.test import TestCase

# Create your tests here.
from miapp.models import Ejercicio

class EjercicioTestCase(TestCase):
    def setUp(self):
        Ejercicio.objects.create(nombre="Martillo Biceps", video_url="https://www.youtube.com/watch?v=KJCvFBsV1ew")
        Ejercicio.objects.create(nombre="Press Militar", video_url="https://www.youtube.com/watch?v=laTnegu5ls8")

    def test_ejercicio_nombre(self):
        ejercicio1 = Ejercicio.objects.get(video_url="https://www.youtube.com/watch?v=KJCvFBsV1ew")
        ejercicio2 = Ejercicio.objects.get(video_url="https://www.youtube.com/watch?v=laTnegu5ls8")
        self.assertEqual(ejercicio1.nombre, 'Martillo Biceps')
        self.assertEqual(ejercicio2.nombre, 'Press Banca')

