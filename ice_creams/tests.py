from django.test import TestCase
from django.urls import reverse
from django.test import RequestFactory, TestCase
from ice_creams.models import *
from django.contrib.auth.models import User
from ice_creams.forms import CreateIceCreamForm
from ice_creams.views import *


class IceCreamViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        number_of_icecreams = 4
        for i in range(number_of_icecreams):
            IceCream.objects.create(
                name=f'Ice Cream {i}',
                description=f'Ice Cream {i} description',
                ingredients=f'Ice Cream {i} ingredients'
            )

        test_user1 = User.objects.create_user(
            username='testuser1', password='')
        test_user1.save()

        self.factory = RequestFactory()

    def test_view_url_info(self):
        response = self.client.get(reverse('info', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_url_info_not_accessible(self):
        response = self.client.get(
            reverse('info', kwargs={'id': IceCream.objects.latest('id').id+1}))
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('new_order'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_order_view(self):
        login = self.client.login(username='testuser1', password='')
        response = self.client.get(reverse('new_order'))
        self.assertEqual(response.status_code, 200)

    def test_create_form_name_field_label(self):
        form = CreateIceCreamForm()
        self.assertTrue(form.fields['name'].label == 'Name')

    def test_create_form_post(self):
        self.client.login(username='testuser1', password='')
        test_ice_cream_name = "my new ice cream"
        response = self.client.post(
            reverse('create'), data={"name": test_ice_cream_name, "description": "my description", "ingredients": "my ingredients"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(IceCream.objects.latest(
            'name').name, test_ice_cream_name)

    def test_add_favorite_post_request_using_info_function(self):
        test_user_name = "testuser1"
        test_ice_cream_id = 2
        self.client.login(username=test_user_name, password='')
        user = User.objects.get(username=test_user_name)
        request = self.factory.post(
            reverse('info', kwargs={'id': test_ice_cream_id}), data={'add_favorite': ['']})
        request.user = user
        response = info(request, test_ice_cream_id)

        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        userprofile = UserProfile.objects.get(user=user)
        self.assertGreater(len(userprofile.favorites.all()), 0)
        self.assertIn(IceCream.objects.get(
            pk=test_ice_cream_id), userprofile.favorites.all())
