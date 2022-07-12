import re
from rest_framework.test import APITestCase
from .models import CustomUser, UserProfile
from message.tests import create_image, SimpleUploadedFile

class TestUserInfo(APITestCase):
    profile_url = "/user/profile"
    file_upload_url = "/message/file-upload"
    login_url = "/user/login"

    def setUp(self):
        payload = {
            "email": "admin@mail.ru",
            "password": "admin",
        }

        self.user = CustomUser.objects._create_user(**payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])}

    # def test_post_user_profile(self):
    #     print(self.user)
    #     payload = {
    #         "user_id": self.user.id,
    #         "first_name": "Uchqun",
    #         "last_name": "Usmonov",
    #         "caption": "Python Developer",
    #     }

    #     response = self.client.post(
    #         self.profile_url, data=payload, **self.bearer)
    #     result = response.json()

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(result["first_name"], "Uchqun")
    #     self.assertEqual(result["last_name"], "Usmonov")
    #     self.assertEqual(result["user"]["email"], "admin@mail.ru")

    # def test_post_user_profile_with_profile_picture(self):

    #     # upload image
    #     avatar = create_image(None, 'avatar.png')
    #     avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
    #     data = {
    #         "file_upload": avatar_file
    #     }

    #     # processing
    #     response = self.client.post(
    #         self.file_upload_url, data=data, **self.bearer)
    #     result = response.json()

    #     payload = {
    #         "user_id": self.user.id,
    #         "first_name": "Uchqun",
    #         "last_name": "Usmonov",
    #         "caption": "Python Developer",
    #         "profile_picture_id": result["id"]
    #     }

    #     response = self.client.post(
    #         self.profile_url, data=payload, **self.bearer)
    #     result = response.json()

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(result["first_name"], "Uchqun")
    #     self.assertEqual(result["last_name"], "Usmonov")
    #     self.assertEqual(result["user"]["email"], "admin@mail.ru")
    #     self.assertEqual(result["profile_picture"]["id"], 1)

    # def test_update_user_profile(self):
    #     # create profile

    #     payload = {
    #         "user_id": self.user.id,
    #         "first_name": "Uchqun",
    #         "last_name": "Usmonov",
    #         "caption": "Python Developer",
    #     }

    #     response = self.client.post(
    #         self.profile_url, data=payload, **self.bearer)
    #     result = response.json()
    #     print('\\\\\\', result)

    #     # --- created profile

    #     payload = {
    #         "first_name": "Uchqun1",
    #         "last_name": "Usmonov1",
    #     }

    #     response = self.client.patch(
    #         self.profile_url + f"/{result['id']}", data=payload, **self.bearer)
    #     result = response.json()

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(result["first_name"], "Uchqun1")
    #     self.assertEqual(result["last_name"], "Usmonov1")
    #     self.assertEqual(result["user"]["email"], "admin@mail.ru")

    def test_user_search(self):

        UserProfile.objects.create(user=self.user, first_name="Adefemi", last_name="oseni",
                                   caption="live is all about living")

        user2 = CustomUser.objects._create_user(
            email="tester@mail.ru", password="tester123", name="testes")
        UserProfile.objects.create(user=user2, first_name="Vester", last_name="Mango",
                                   caption="it's all about testing")

        user3 = CustomUser.objects._create_user(
            email="vasman@mail.ru", password="vasman123", name="vasman")
        UserProfile.objects.create(user=user3, first_name="Adeyemi", last_name="Boseman",
                                   caption="it's all about testing")

        # test keyword = adefemi oseni
        url = self.profile_url + "?keyword=adefemi oseni"

        response = self.client.get(url, **self.bearer)
        result = response.json()['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)

        # test keyword = ade
        url = self.profile_url + "?keyword=ade"

        response = self.client.get(url, **self.bearer)
        result = response.json()['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["user"]["email"], "vasman@mail.ru")

        # test keyword = vester
        url = self.profile_url + "?keyword=vester"

        response = self.client.get(url, **self.bearer)
        result = response.json()['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["user"]["email"], "tester@mail.ru")