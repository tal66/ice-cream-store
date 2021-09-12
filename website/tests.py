from django.test import TestCase
from django.urls import reverse
from ice_creams.models import IceCream
from django.contrib.auth.models import User


class HompageViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        number_of_icecreams = 4
        for i in range(1, number_of_icecreams+1):
            IceCream.objects.create(
                name=f'Ice Cream {i}',
                description=f'Ice Cream {i} description',
                ingredients=f'Ice Cream {i} ingredients'
            )

        test_user1 = User.objects.create_user(
            username='testuser1', password='')
        test_user1.save()

    def test_view_homepage_status_ok(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_view_home_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'home.html')

    def test_view_ice_cream_list_on_homepage(self):
        response = self.client.get(reverse('homepage'))
        icecreams = response.context['all_ice_creams']
        self.assertEqual(len(icecreams), len(IceCream.objects.all()))
        self.assertEqual(icecreams[0], IceCream.objects.get(pk=1))
