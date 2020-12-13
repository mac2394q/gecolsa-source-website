from test_plus.test import TestCase
from django_dynamic_fixture import G

from cms.models import Communication
from cms.models import CommunicationCategory
from cms.models import Page
from cms.models import CommunicationNews
from cms.models import FeaturedContent
from common.models import FixedBlock
from userprofile.models import User


class CmsTestCase(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='password',
        )

        self.communication_article = G(
            Communication,
        )

        G(
            FixedBlock,
            slug='communication',
        )

        # Pages referenced from home.
        for slug in [
            'nosotros',
            'industrias',
            'repuestos-y-servicios',
            'financiacion',
            'renta',
            'legal',
            'tecnologia',
        ]:
            page = G(
                Page,
                is_active=True,
                content='Test page',
                show_children=False,
            )
            page.slug = slug
            page.save()

        self.communicationnews = G(
            CommunicationNews,
            is_active=True,
        )

    def test_category_comments(self):
        self.communication_article.category.has_comments = False
        self.communication_article.category.save()
        response = self.get(
            self.communication_article.get_absolute_url(),
        )
        self.assertNotContains(
            response,
            '<div class="disqus-thread" id="disqus_thread">'
        )

        # With comments.
        self.communication_article.category.has_comments = True
        self.communication_article.category.save()
        response = self.get(
            self.communication_article.get_absolute_url(),
        )
        self.assertContains(
            response,
            '<div class="disqus-thread" id="disqus_thread">'
        )

    def test_communication_is_active(self):
        response = self.get(
            self.communicationnews.get_absolute_url(),
        )
        self.response_200(response)

        # Inactive news.
        self.communicationnews.is_active = False
        self.communicationnews.save()
        response = self.get(
            self.communicationnews.get_absolute_url(),
        )
        self.response_404(response)

        # Active page.
        page = Page.objects.filter(is_active=True, show_children=False).first()
        response = self.get(
            page.get_absolute_url(),
        )
        self.response_200(response)

        # Inactive page.
        page.is_active = False
        page.save()
        response = self.get(
            page.get_absolute_url(),
        )
        self.response_404(response)

    def test_category_share_buttons(self):
        self.communication_article.category.has_share_buttons = False
        self.communication_article.category.save()
        response = self.get(
            self.communication_article.get_absolute_url(),
        )
        self.assertNotContains(
            response,
            '<div class="addthis_inline_share_toolbox">'
        )

        # With share buttons.
        self.communication_article.category.has_share_buttons = True
        self.communication_article.category.save()
        response = self.get(
            self.communication_article.get_absolute_url(),
        )
        self.assertContains(
            response,
            '<div class="addthis_inline_share_toolbox">'
        )

    def test_communication_categories_links(self):
        communication2 = G(
            Communication,
            is_active=False,
        )
        response = self.get(
            'cms:communication_list',
        )
        self.assertNotContains(
            response,
            '<a href="{0}">'.format(
                communication2.get_absolute_url(),
            )
        )

        communication2.is_active = True
        communication2.save()
        response = self.get(
            'cms:communication_list',
        )
        self.assertContains(
            response,
            '<a href="{0}">'.format(
                communication2.get_absolute_url(),
            )
        )

        communication_category = G(CommunicationCategory)

        response = self.get(
            'cms:communication_by_category_list',
            communication_category.slug,
        )
        self.response_200(response)

    def test_featured_content_admin(self):
        """ Test opening featured content admin and make sure
            we cannot add more items.
        """
        featured_content = G(
            FeaturedContent,
            title='GECOLSA, SU ALIADO',
            is_external=True,
            url='https://google.com'
        )
        G(FeaturedContent)
        G(FeaturedContent)
        G(
            FeaturedContent,
            title='COMPRÉ CON DESCUENTO UNA MISMA CALIDAD',
            is_external=True,
            url='https://google4.com'
        )

        with self.login(email=self.admin.email):
            response = self.get(
                'admin:cms_featuredcontent_changelist',
            )

            self.assertContains(
                response,
                'class="addlink"',
            )

            # Detail.
            response = self.get(
                'admin:cms_featuredcontent_change',
                featured_content.id,
            )
            self.assertContains(
                response,
                'name="_addanother"',
            )

            response = self.get(
                'home',
            )

            self.assertContains(
                response,
                'GECOLSA, SU ALIADO',
            )

            self.assertNotContains(
                response,
                'COMPRÉ CON DESCUENTO UNA MISMA CALIDAD',
            )

        # Make sure it's visible in the home page
        # and have the propper links.
        response = self.get('home')
        self.assertContains(
            response,
            'href="https://google.com" target="_blank"'
        )
        featured_content.is_external = False
        featured_content.save()

        response = self.get('home')
        self.assertContains(
            response,
            'href="https://google.com" >'
        )

    def test_satellite_monitoring_contact_view(self):
        response = self.get(
            'satellital_tracking',
        )
        self.response_200(response)

    def test_post_satellite_monitoring_contact_view(self):
        response = self.post(
            'satellital_tracking',
            data={
                'name': 'test name',
                'company': 'test company name',
                'email': 'test@email.com',
                'phone': '3111111111',
                'address': 'tesst address',
                'machine': 'test machine',
            },
        )
        self.response_302(response)

    def test_report_satellite_xls_view(self):
        with self.login(email=self.admin.email):
            response = self.get(
                'download_satellite_report',
            )
            self.response_302(response)
