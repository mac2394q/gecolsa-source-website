from django.conf import settings
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView

import re

from app.utils import send_email
from common.forms import ContactForm
from common.forms import OfficeForm
from common.models import Office


class ContactView(TemplateView):
    template_name = 'common/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        office_form = OfficeForm()
        office_form.fields['city'].label = ''
        context['office_form'] = office_form
        context['form'] = ContactForm

        return context


class ContactFormView(FormView):
    form_class = ContactForm

    def get(self, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        pattern = re.compile(r'(?!&)utm_[^=]*=[^&]*(?=&|$)')
        obj = form.save()
        obj.recipients = settings.DEFAULT_TO_EMAIL[0]
        obj.save()
        utm_list = re.findall(pattern, obj.full_path.rstrip())

        utm_dict = {}
        if utm_list:
            utm_dict = {
                utm.split('=')[0]: utm.split('=')[1] for utm in utm_list
            }

        send_email(
            '[GECOLSA] Contacto desde el portal web',
            [form.instance.email],
            'common/contact_email_user.html',
            {'contact': form.instance},
        )

        send_email(
            '[GECOLSA] Contacto desde el portal web',
            settings.DEFAULT_TO_EMAIL,
            'common/contact_email.html',
            {'contact': form.instance, 'utm_dict': utm_dict},
        )

        return JsonResponse({
            'ok': True,
            'message': 'Gracias por su interés, pronto le contactaremos.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'ok': False,
            'message': form.errors
        })


class OfficeListView(ListView):
    model = Office
    context_object_name = 'offices'
    search_city = None

    def dispatch(self, request, *args, **kwargs):
        """If is filtering by city check if the city is valid
        otherwise it will redirect the user to the office_list
        page.
        """
        if 'city' in request.GET and request.GET['city']:
            try:
                city_id = int(request.GET['city'])
            except ValueError:
                # Bad parameter
                return redirect('office_list')

            queryset = self.get_queryset().filter(city_id=city_id)
            if queryset:
                self.search_city = queryset.first().city
            else:
                # There are no offices matching the filter
                return redirect('office_list')

        return super(OfficeListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(OfficeListView, self).get_queryset()

        queryset = queryset.filter(is_active=True)
        if self.search_city:
            queryset = queryset.filter(city=self.search_city)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(OfficeListView, self).get_context_data(**kwargs)

        if self.search_city:
            office_form = OfficeForm(initial={'city': self.search_city})
        else:
            office_form = OfficeForm()

        context['office_form'] = office_form
        context['search_city'] = self.search_city

        return context
