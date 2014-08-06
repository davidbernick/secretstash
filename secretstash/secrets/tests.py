from django.contrib.auth.models import User,Group,Permission
from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework import status
import json


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.regularuser = User.objects.create_user(
            username='randomtestuser', email='randomtestuser@asdf.com', password='top_secret')

        self.adminuser = User.objects.create_user(
            username='randomtestadmin', email='randomtestadmin@asdf.com', password='top_secret')

        self.baduser = User.objects.create_user(
            username='badtestuser', email='badtestuser@asdf.com', password='top_secret')

        self.group = Group(name="testgroup")
        self.group.save()

        self.group2 = Group(name="testgroup2")
        self.group2.save()


        self.admingroup = Group(name="testadmin")
        self.admingroup.save()

        self.regularuser.groups.add(self.group)
        self.adminuser.groups.add(self.admingroup)
        self.adminuser.groups.add(self.group)
        self.baduser.groups.add(self.group2)
        
        permission = Permission.objects.get(codename='add_host')
        self.admingroup.permissions.add(permission)

        self.client = APIClient()
        self.client.login(username='randomtestuser', password='top_secret')

        self.adminclient = APIClient()
        self.adminclient.login(username='randomtestadmin', password='top_secret')

        self.badclient = APIClient()
        self.badclient.login(username='badtestuser', password='top_secret')
        
        response = self.client.post('/secrets/api/secret/', {"groups":["testgroup"],"description":"AWS key for bucket1 r/w access","content":"AKIAasdfasdf","name":"aws_key_s3_bucket1"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.secret_id=json.loads(response.content)["id"]
        self.secret_name=json.loads(response.content)["name"]

    def test_get_secret(self):
        response = self.client.get('/secrets/api/secret/%s/' % self.secret_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_secret_bad(self):
        response = self.badclient.get('/secrets/api/secret/%s/' % self.secret_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
#     def test_patch(self):
#         response = self.adminclient.patch('/secrets/api/secret/%s/' % self.secret_id,{"groups":["testgroup2"]},format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
# 
#     def test_patch_get_bad_redux(self):
#         response = self.badclient.get('/secrets/api/secret/%s/' % self.secret_id)
#         print self.secret_id
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

