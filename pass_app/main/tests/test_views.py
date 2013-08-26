from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from pagetree.models import Hierarchy
from pass_app.main.views import Column


class LoggedOutTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
        self.assertEqual(response.status_code, 302)


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

    def test_instructor_page_post(self):
        self.u.is_superuser = True
        self.u.save()
        response = self.c.post("/instructor/module-one/")
        self.assertEqual(response.status_code, 200)
        response = self.c.post("/instructor/module-one/",
                               dict(clear=0))
        self.assertEqual(response.status_code, 404)

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
        h = Hierarchy.objects.create(name="main", base_url="")
        h.get_root().add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        response = self.c.get("/admin/allresults/?format=csv")
        self.assertEqual(response.status_code, 200)

    def test_all_results_key(self):
        response = self.c.get("/admin/allresultskey/")
        self.assertEqual(response.status_code, 403)
        self.u.is_staff = True
        self.u.save()
        response = self.c.get("/admin/allresultskey/")
        self.assertEqual(response.status_code, 200)
        h = Hierarchy.objects.create(name="main", base_url="")
        h.get_root().add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })
        response = self.c.get("/admin/allresultskey/")
        self.assertEqual(response.status_code, 200)


class Actor(object):
    def __init__(self, t="IV"):
        self.type = t
        self.id = "actor"


class ColumnTest(TestCase):
    def setUp(self):
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.h.get_root().add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'children': [{'label': "Three", 'slug': "introduction"}]
             })

    def test_create(self):
        c = Column(self.h)
        self.assertTrue(c is not None)

    def test_actor_id(self):
        c = Column(self.h, actor=Actor())
        self.assertEqual(c.actor_id(), "%s_stakeholder_actor" % self.h.id)
        c = Column(self.h, actor=Actor("BD"))
        self.assertEqual(c.actor_id(), "%s_boardmember_actor" % self.h.id)
        c = Column(self.h, actor=Actor("DS"))
        self.assertEqual(c.actor_id(), "%s_defend_strategy" % self.h.id)

    def test_key_row(self):
        class AQ(object):
            id = "bar"
            question = "a question"

        c = Column(self.h)
        self.assertEqual(
            c.key_row(),
            ['1_last_visited', u'One', 'short text', 'Last Visited Date'])
        c = Column(self.h, actor=Actor("DS"), actor_question=AQ())
        self.assertEqual(
            c.key_row(),
            ['1_defend_strategy_bar', u'One', 'short text', 'a question'])

    def test_header_column(self):
        c = Column(self.h)
        self.assertEqual(
            c.header_column(),
            ['1_last_visited'])
