from django.contrib.auth.models import User
from pass_app.careerlocation.models import CareerLocationState
from tastypie.test import ResourceTestCase


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
        url = '/api/v1/career_location_state/%s/' % (self.cls1.id)
        response = self.api_client.get(url, format='json')
        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(json['user'],
                          "/api/v1/user/%s/" % self.user1.id)

        # get someone else's
        url = '/api/v1/career_location_state/%s/' % (self.cls2.id)
        response = self.api_client.get(url, format='json')
        self.assertEquals(response.status_code, 401)

    def test_get_list(self):
        self.assertTrue(
            self.api_client.client.login(username="test_student_one",
                                         password="test"))

        url = '/api/v1/career_location_state/'
        response = self.api_client.get(url, format='json')

        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(len(json['objects']), 1)
        self.assertEquals(json['objects'][0]['user'],
                          "/api/v1/user/%s/" % self.user1.id)
