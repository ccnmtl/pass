from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from pagetree.models import Hierarchy, Section
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
        Hierarchy.objects.all().delete()
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
        Hierarchy.objects.all().delete()
        response = self.c.get("/admin/allresultskey/")
        self.assertEqual(response.status_code, 200)
        Hierarchy.objects.all().delete()
        h = Hierarchy.objects.create(name="main", base_url="")
        h.get_root().add_child_section_from_dict(
            {'label': "One", 'slug': "socialwork",
             'pageblocks': [],
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

    def tearDown(self):
        Section.objects.all().delete()
        Hierarchy.objects.all().delete()

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
        key_row = c.key_row()
        self.assertTrue(key_row[0].endswith('last_visited'))
        self.assertEqual(key_row[1], u'One')
        self.assertEqual(key_row[2], 'short text')
        self.assertEqual(key_row[3], 'Last Visited Date')

        c = Column(self.h, actor=Actor("DS"), actor_question=AQ())
        key_row = c.key_row()
        self.assertTrue(key_row[0].endswith('defend_strategy_bar'))
        self.assertEqual(key_row[1], u'One')
        self.assertEqual(key_row[2], 'short text')
        self.assertEqual(key_row[3], 'a question')

    def test_header_column(self):
        c = Column(self.h)
        self.assertTrue(c.header_column()[0].endswith('last_visited'))
