from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APISimpleTestCase


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200


class BondTests(TestCase):
    data = {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
    }

    def test_get_bonds(self):
        resp = self.client.get(reverse('bonds'))
        assert resp.status_code == status.HTTP_200_OK

    def test_post_valid_bond(self):
        self.data['lei'] = "R0MUWSFPU8MPRO8K5P83"
        resp = self.client.post(reverse('bonds'), self.data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_post_incomplete_regex_lei_bond(self):
        self.data['lei'] = "ROM"
        resp = self.client.post(reverse('bonds'), self.data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_regex_lei_bond(self):
        self.data['lei'] = "R0MUWSFPU8MPRO8K5P83"[::-1]
        resp = self.client.post(reverse('bonds'), self.data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
