from django.contrib import messages
from django.contrib.sites.models import Site
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.html import strip_tags
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View


from braces.views import SuperuserRequiredMixin
from constance import config

from app.utils import send_email
from cms.forms import SatelliteMonitoringContactForm
from cms.models import Communication
from cms.models import CommunicationCategory
from cms.models import Page
from cms.models import SatelliteMonitoringContact
from cms.tasks import task_send_satellite_report
from common.forms import ContactForm


class CommunicationListView(ListView):
    model = Communication
    context_object_name = 'communications'
    communication_category = None

    def dispatch(self, request, *args, **kwargs):
        if 'slug' in self.kwargs and self.kwargs['slug']:
            try:
                self.communication_category = \
                    CommunicationCategory.objects.get(slug=self.kwargs['slug'])
            except CommunicationCategory.DoesNotExist:
                self.communication_category = None
        return super(
            CommunicationListView,
            self,
        ).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(CommunicationListView, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        if self.communication_category:
            queryset = queryset.filter(category=self.communication_category)
        return queryset.select_related('category')

    def get_context_data(self, **kwargs):
        context = super(CommunicationListView, self).get_context_data(**kwargs)
        context['communication_categories'] = \
            CommunicationCategory.objects.filter(
                communication__is_active=True,
        ).distinct()
        context['current_communication_category'] = self.communication_category
        return context


class CommunicationDetailView(DetailView):
    model = Communication
    context_object_name = 'communication'

    def get(self, *args, **kwargs):
        if not self.get_object().is_active:
            raise Http404
        return super(
            CommunicationDetailView,
            self,
        ).get(*args, **kwargs)


class PageDetailView(DetailView):
    model = Page
    context_object_name = 'page'

    def get(self, *args, **kwargs):
        if not self.get_object().is_active:
            raise Http404
        if (
            not self.get_object().children.exists() and
            not strip_tags(self.get_object().content)
        ):
            if self.get_object().parent:
                return redirect(reverse(
                    'cms:page_detail',
                    args=[self.get_object().parent.slug]
                ))
            else:
                raise Http404

        return super(
            PageDetailView,
            self,
        ).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


class SatelliteMonitoringContactView(CreateView):
    template_name = 'cms/satellite_monitoring.html'
    model = SatelliteMonitoringContact
    form_class = SatelliteMonitoringContactForm
    success_url = reverse_lazy('home')
    bcc_list = None

    def dispatch(self, request, *args, **kwargs):
        self.bcc_list = [config.EMAIL_SATELITAL]
        return super(
            SatelliteMonitoringContactView,
            self
        ).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        site = Site.objects.get_current().name
        send_email(
            '[{0}] Registro de monitoreo satelital'.format(site),
            [form.instance.email],
            'cms/satellite_monitoring_email.html',
            {'contact': form.instance},
            from_addr=config.EMAIL_SATELITAL,
            bcc_mails=self.bcc_list,
        )
        messages.info(
            self.request,
            'Gracias por su interés, pronto le contactaremos.',
        )

        return super(SatelliteMonitoringContactView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SatelliteMonitoringContactView, self).get_context_data(
            **kwargs
        )
        context['email_contact'] = self.bcc_list[0]

        return context


class ReportSatelliteXls(SuperuserRequiredMixin, View):
    def get(self, *args, **kwargs):
        task_send_satellite_report.delay(
            [self.request.user.email],
        )
        messages.info(
            self.request,
            'Recibirá un correo con la información solicitada',
        )

        return HttpResponseRedirect(reverse('admin:index'))
