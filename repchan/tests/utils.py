# -*- encoding: utf-8
from django.test import TestCase

class TestCaseVersion(TestCase):

    def assertCountObject(self, number_of_objects, model):
        self.assertEqual(number_of_objects, len(model.objects.all()))
        self.assertEqual(number_of_objects, model.objects.count())

    def assertCountObjectInTrash(self, number_of_objects, model):
        self.assertEqual(number_of_objects, len(model.objects.in_trash()))
        self.assertEqual(number_of_objects, model.objects.in_trash().count())
