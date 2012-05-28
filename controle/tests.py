# -*- encoding : utf-8 -*-

from django.utils import unittest
from django.forms.models import model_to_dict
from controle.models import Controle
#from controle.models import Conta


class ControleTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_criar_novo_controle(self):
        expected_attrs = {'ano': 2012, 'mes': 3}
        Controle.objects.create(**expected_attrs)
        gotten_attrs = model_to_dict(Controle.objects.get(**expected_attrs))
        del gotten_attrs['id']

        self.assertDictEqual(expected_attrs, gotten_attrs)
