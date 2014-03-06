#pylint: disable-msg=R0904
#pylint: disable-msg=E1103
from django.contrib.auth.models import User
from pass_app.careerlocation.models import CareerLocationState
from tastypie.test import ResourceTestCase


class UserResourceTest(ResourceTestCase):

    def setUp(self):
        super(UserResourceTest, self).setUp()

        self.user1 = User.objects.create_user('test_student_one',
                                              'test@ccnmtl.com',
                                              'test')
        self.user1.save()

        self.user2 = User.objects.create_user('test_student_two',
                                              'test@ccnmtl.com',
                                              'test')
        self.user2.save()

    def get_credentials(self):
        return None

    def test_get_object(self):
        self.assertTrue(
            self.api_client.client.login(username="test_student_one",
                                         password="test"))

        # get mine
        url = '/_careerlocation/api/v1/user/%s/' % (self.user1.id)
        response = self.api_client.get(url, format='json')

        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(json['username'], 'test_student_one')

        # get someone else's
        url = '/_careerlocation/api/v1/user/%s/' % (self.user2.id)
        response = self.api_client.get(url, format='json')
        self.assertEquals(response.status_code, 401)

    def test_get_list(self):
        self.assertTrue(
            self.api_client.client.login(username="test_student_one",
                                         password="test"))

        url = '/_careerlocation/api/v1/user/'
        response = self.api_client.get(url, format='json')

        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(len(json['objects']), 1)
        self.assertEquals(json['objects'][0]['username'], 'test_student_one')


class CareerLocationStateResourceTest(ResourceTestCase):

    def setUp(self):
        super(CareerLocationStateResourceTest, self).setUp()

        self.user1 = User.objects.create_user('test_student_one',
                                              'test@ccnmtl.com',
                                              'test')
        self.user1.save()
        self.cls1 = CareerLocationState.objects.create(user=self.user1)

        self.user2 = User.objects.create_user('test_student_two',
                                              'test@ccnmtl.com',
                                              'test')
        self.user2.save()
        self.cls2 = CareerLocationState.objects.create(user=self.user2)

    def get_credentials(self):
        return None

    def test_get_object(self):
        self.assertTrue(
            self.api_client.client.login(username="test_student_one",
                                         password="test"))

        # get mine
        url = '/_careerlocation/api/v1/career_location_state/%s/' % (
            self.cls1.id)
        response = self.api_client.get(url, format='json')
        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(json['user'],
                          "/_careerlocation/api/v1/user/%s/" % self.user1.id)

        # get someone else's
        url = '/_careerlocation/api/v1/career_location_state/%s/' % (
            self.cls2.id)
        response = self.api_client.get(url, format='json')
        self.assertEquals(response.status_code, 401)

    def test_get_list(self):
        self.assertTrue(
            self.api_client.client.login(username="test_student_one",
                                         password="test"))

        url = '/_careerlocation/api/v1/career_location_state/'
        response = self.api_client.get(url, format='json')

        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(len(json['objects']), 1)
        self.assertEquals(json['objects'][0]['user'],
                          "/_careerlocation/api/v1/user/%s/" % self.user1.id)
