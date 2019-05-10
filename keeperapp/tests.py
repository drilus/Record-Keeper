from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from keeperapp.models import Profile, Category, CategoryInfo, Record
import json


class KeeperApp(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='pianonecktie',
            password='testing',
            first_name='Jacobi',
            last_name='Mugatu',
            email='jmugatu@pianotie.com'
        )
        cls.profile = Profile.objects.create(
            user=cls.user,
            phone='812-555-1212',
            address='1001 Piano Neck Tie Inc',
            city='Louisville',
            state='Kentucky',
            zip='32571',
            avatar=None
        )
        cls.category = Category.objects.create(
            user=cls.user,
            name='Test Category',
            columns='Name, Cost, Date',
            options=json.loads('{"null":"null"}')
        )
        cls.category_info = CategoryInfo.objects.create(
            category=cls.category,
            description='test category',
            image=None,
            file=None
        )
        cls.record = Record.objects.create(
            user=cls.user,
            category=cls.category,
            data=json.loads('{"Name": "Test Record", "Cost": "57.68", "Date": "2019/05/09"}')
        )

    def test_profile_avatar(self):
        profile = self.profile
        self.assertTrue(profile.avatar_url == '/static/img/default-profile-icon-24.jpg')
        self.assertTrue(profile.user.username == 'pianonecktie')

    def test_category_image(self):
        category_info = self.category_info
        self.assertTrue(category_info.image_url == '/static/img/699086-icon-94-folder-512.png')


class ViewTemplates(KeeperApp):
    def setUp(self):
        self.client = Client()
        self.client.login(username=self.user.username, password='testing')

    def test_login(self):
        user_login = self.client.login(username=self.user.username, password='testing')
        self.assertTrue(user_login)

    def test_user_main_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('user_main'))
        self.assertEquals(response.status_code, 302)

    def test_user_sign_up_uses_correct_template(self):
        response = self.client.get(reverse('user-sign-up'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/sign_up.html')

    def test_user_overview_uses_correct_template(self):
        response = self.client.get(reverse('user-overview'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/overview.html')

    def test_user_settings_uses_correct_template(self):
        response = self.client.get(reverse('user-settings'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/settings.html')

    def test_user_categories_uses_correct_template(self):
        response = self.client.get(reverse('user-categories'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/categories.html')

    def test_edit_category_uses_correct_template(self):
        response = self.client.get(reverse('edit-category', kwargs={'category_id': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/edit_category.html')

    def test_add_category_uses_correct_template(self):
        response = self.client.get(reverse('add-category'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_category.html')

    def test_user_records_uses_correct_template(self):
        response = self.client.get(reverse('user-records'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/records.html')

    def test_add_record_uses_correct_template(self):
        response = self.client.get(reverse('add-record'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/add_record.html')

    def test_user_category_records_uses_correct_template(self):
        response = self.client.get(reverse('records-info', kwargs={'category_id': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/record_info.html')

    def test_edit_record_uses_correct_template(self):
        response = self.client.get(reverse('edit-record', kwargs={'record_id': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/edit_record.html')
