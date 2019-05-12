from django.test import Client, TestCase, LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User

from keeperapp.models import Profile, Category, CategoryInfo, Record, Option
from keeperapp.forms import UserCreationForm, ProfileForm, CategoryForm, CategoryInfoForm

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        cls.option = Option(
            user=cls.user,
            view='test-view',
            theme='monokai'
        )


class ViewTemplatesGet(KeeperApp):
    def setUp(self):
        self.client = Client()
        self.client.login(username=self.user.username, password='testing')

    def test_login(self):
        user_login = self.client.login(username=self.user.username, password='testing')
        self.assertTrue(user_login)

    def test_user_main_status_code(self):
        response = self.client.get(reverse('user-home'), follow=True)
        self.assertRedirects(response, reverse('user-overview'), status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

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


class FormsTest(KeeperApp):
    def test_user_sign_up(self):
        user_data = {
            'username': 'dzoolander',
            'first_name': 'Derek',
            'last_name': 'Zoolander',
            'email': 'dzoolander@derelict.com',
            'password1': '*fuaqGiz3X7c&ftU&823',
            'password2': '*fuaqGiz3X7c&ftU&823'
        }
        profile_data = {
            'phone': '555-1212',
            'address': 'Hollywood',
            'city': 'Las Angelas',
            'state': 'California',
            'zip': '55555'
        }
        user_form = UserCreationForm(data=user_data)
        profile_form = ProfileForm(data=profile_data)
        self.assertTrue(user_form.is_valid())
        self.assertTrue(profile_form.is_valid())
        # sys.stderr.write(repr(object_to_print) + '\n')

    def test_category_form(self):
        category = {
            'name': 'Test Name',
            'columns': 'Price, Total, Date',
            'options': '{"null": "null"}'
        }
        category_form = CategoryForm(data=category)
        self.assertTrue(category_form.is_valid())

    def test_category_info_form(self):
        cat_info = {
            'description': 'Test description',
            'image': None,
            'file': None
        }
        info_form = CategoryInfoForm(data=cat_info)
        self.assertTrue(info_form.is_valid())


class ModelTest(KeeperApp):
    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), self.category.name)

    def test_profile_creation(self):
        profile = self.profile
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(profile.avatar_url, '/static/img/default-profile-icon-24.jpg')
        self.assertEqual(profile.user.username, 'pianonecktie')
        self.assertEqual(profile.__str__(), profile.user.username)

    def test_category_info_creation(self):
        category_info = self.category_info
        self.assertTrue(isinstance(category_info, CategoryInfo))
        self.assertEqual(category_info.image_url, '/static/img/699086-icon-94-folder-512.png')
        self.assertEqual(category_info.__str__(), str(category_info.id))

    def test_record_creation(self):
        record = self.record
        self.assertTrue(isinstance(record, Record))
        self.assertTrue(record.category, self.category)
        self.assertEqual(record.__str__(), str(record.id))

    def test_option_creation(self):
        option = self.option
        self.assertEqual(option.__str__(), option.user.username)


class ViewTestNoTestData(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='pianonecktie',
            password='testing',
            first_name='Jacobi',
            last_name='Mugatu',
            email='jmugatu@pianotie.com'
        )
        self.client = Client()
        self.client.login(username=self.user.username, password='testing')

    def test_user_category_records_count(self):
        self.category = Category.objects.create(
            user=self.user,
            name='Test Category',
            columns='Name, Cost, Date',
            options=json.loads('{"null":"null"}')
        )
        response = self.client.get(reverse('records-info', kwargs={'category_id': 1}), follow=True)
        self.assertRedirects(response, reverse('add-record'), status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)


class ViewTesting(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.PhantomJS()
        super(ViewTesting, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(ViewTesting, self).tearDown()

    def test_account_signup(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/user/sign-up')
        username = selenium.find_element_by_id('id_username')
        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        phone = selenium.find_element_by_id('id_phone')
        address = selenium.find_element_by_id('id_address')
        city = selenium.find_element_by_id('id_city')
        state = selenium.find_element_by_id('id_state')
        zipcode = selenium.find_element_by_id('id_zip')

        submit = selenium.find_element_by_name('register')

        username.send_keys('derelict')
        first_name.send_keys('Derek')
        last_name.send_keys('Zoolander')
        email.send_keys('dzoolander@derelict.com')
        password1.send_keys('6jX*5XCd*E4c*aa9xhXV')
        password2.send_keys('6jX*5XCd*E4c*aa9xhXV')
        phone.send_keys('555-1212')
        address.send_keys('512 Fashion Model Park')
        city.send_keys('Las Angelas')
        state.send_keys('California')
        zipcode.send_keys('16823')

        submit.click()
        # selenium.save_screenshot('screenshot.png')

        wait = WebDriverWait(selenium, 10)
        wait.until(EC.url_changes('http://127.0.0.1:8000/user/sign-up'))
        url = selenium.current_url
        self.assertEqual(url, 'http://127.0.0.1:8000/user/overview')
