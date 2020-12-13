from test_plus.test import TestCase

from django_dynamic_fixture import G

from cms.models import Page
from common.models import FixedBlock


class AppTestCase(TestCase):

    def setUp(self):
        G(Page, slug='nosotros')
        G(Page, slug='industrias')
        G(Page, slug='repuestos-y-servicios')
        G(Page, slug='financiacion')
        G(Page, slug='legal')
        G(Page, slug='renta')
        G(Page, slug='tecnologia')
        G(FixedBlock, slug='contact')
        G(FixedBlock, slug='slide_home')

    def test_frontpage(self):
        """Check if the front is correct"""
        response = self.get('home')
        self.response_200(response)

    def test_sitemap(self):
        """Check if the sitemap is correct"""
        response = self.get('/sitemap.xml')
        self.response_200(response)

    def test_contact(self):
        """Checks the contact form"""
        response = self.get('contact')
        self.response_200(response)

        response = self.post(
            'contact_form',
            data={
                'name': 'mr. dine',
                'mobile_number': '3134567892',
                'email': 'dine@dyne.com',
                'comment': 'vamos a tener cosas cheveres',
                'accept_terms': True,
            }
        )

        self.response_200(response)
        self.assertContains(
            response,
            'pronto le contactaremos.'
        )
