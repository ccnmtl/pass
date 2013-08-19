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

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)

    def test_demographic(self):
        response = self.c.get("/demographic/")
        self.assertEquals(response.status_code, 302)

    def test_reports(self):
        response = self.c.get("/admin/reports/")
        self.assertEquals(response.status_code, 403)
        self.u.is_staff = True
        self.u.save()
        response = self.c.get("/admin/reports/")
        self.assertNotEquals(response.status_code, 403)

    def test_page(self):
        response = self.c.get("/module-one/")
        self.assertEqual(response.status_code, 302)

    def test_instructor_page(self):
        response = self.c.get("/instructor/module-one/")
        self.assertEqual(response.status_code, 403)
        self.u.is_superuser = True
        self.u.save()
        response = self.c.get("/instructor/module-one/")
        self.assertEqual(response.status_code, 200)

    def test_edit_page(self):
        response = self.c.get("/edit/module-one/")
        self.assertEqual(response.status_code, 403)
        self.u.is_superuser = True
        self.u.save()
        response = self.c.get("/edit/module-one/")
        self.assertEqual(response.status_code, 200)

    def test_all_results(self):
        response = self.c.get("/admin/allresults/")
        self.assertEqual(response.status_code, 403)
        self.u.is_staff = True
        self.u.save()
        response = self.c.get("/admin/allresults/")
        self.assertEqual(response.status_code, 200)

    def test_all_results_key(self):
        response = self.c.get("/admin/allresultskey/")
        self.assertEqual(response.status_code, 403)
        self.u.is_staff = True
        self.u.save()
        response = self.c.get("/admin/allresultskey/")
        self.assertEqual(response.status_code, 200)
