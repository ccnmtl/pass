from django.contrib.auth.models import User
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
        url = '/api/v1/user/%s/' % (self.user1.id)
        response = self.api_client.get(url, format='json')

        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(json['username'], 'test_student_one')

        # get someone else's
        url = '/api/v1/user/%s/' % (self.user2.id)
        response = self.api_client.get(url, format='json')
        self.assertEquals(response.status_code, 401)

    def test_get_list(self):
        self.assertTrue(
            self.api_client.client.login(username="test_student_one",
                                         password="test"))

        url = '/api/v1/user/'
        response = self.api_client.get(url, format='json')

        self.assertValidJSONResponse(response)
        json = self.deserialize(response)
        self.assertEquals(len(json['objects']), 1)
        self.assertEquals(json['objects'][0]['username'], 'test_student_one')
