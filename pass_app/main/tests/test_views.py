from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class BasicTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def tearDown(self):
        self.u.delete()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

#    def test_smoketest(self):
#        response = self.c.get("/smoketest/")
#        self.assertEquals(response.status_code, 200)
#        assert "PASS" in response.content
