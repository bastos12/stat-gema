from django.test import TestCase
import random
class TestStatistiques(TestCase):
    def setUp(self):
        self.choice = ['1', '2', '3', '4']

    def test_sample_choice(self):
        for i in range(0, 500):
            result = random.sample(population=self.choice, k=2)
            self.assertFalse(result[0] == result[1])