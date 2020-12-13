import os
import json

from django.views.generic import View
from django.views.generic import TemplateView
from django.conf import settings
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_str

from braces.views import SuperuserRequiredMixin

from common.models import SliderHome
from cms.models import Communication
from cms.models import FeaturedContent
from app.forms import ImageForm, RequestsComplaintsForm
from app.utils import send_email

from . import data


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['home_sliders'] = SliderHome.objects.filter(is_active=True)
        context['communications'] = Communication.objects.filter(
            is_active=True,
        )[:6]
        context['featured_content'] = FeaturedContent.objects.all()[:3]
        return context


class CleanCacheView(SuperuserRequiredMixin, View):
    """Limpia el cache usado por la aplicacion.
    """
    def get(self, *args, **kwargs):
        cache.clear()
        messages.info(
            self.request,
            'Se ha regenerado el caché',
        )

        return HttpResponseRedirect(reverse('admin:index'))


class RedactorUploadView(FormView):
    form_class = ImageForm
    http_method_names = ('post',)
    upload_to = 'redactor/'

    @method_decorator(csrf_exempt)
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RedactorUploadView, self).dispatch(
            request, *args, **kwargs)

    def form_invalid(self, form):
        try:
            error = form.errors.values()[-1][-1]
        except:
            error = 'Invalid file.'
        data_dict = {
            'error': error,
        }
        return HttpResponse(json.dumps(data_dict), content_type='application/json')

    def form_valid(self, form):
        upload_file = form.cleaned_data['file']

        full_path = os.path.join(self.upload_to, upload_file.name)
        storage = FileSystemStorage()
        real_path = storage.save(full_path, upload_file)
        file_name = force_str(upload_file.name)

        # get url for file if he saved else None
        file_url = storage.url(real_path)
        data_dict = {
            'filelink': file_url,
            'filename': file_name,
        }
        return HttpResponse(json.dumps(data_dict), content_type='application/json')


class RequestsComplaintsView(FormView):
    form_class = RequestsComplaintsForm
    template_name = 'requests_complaints.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'OTHER_CHOICE': data.OTHER_CHOICE,
            'ANONYMOUS_CHOICE': data.ANONYMOUS_CHOICE,
            'NOT_ANONYMOUS_CHOICE': data.NOT_ANONYMOUS_CHOICE,
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                complaint = form.save(commit=False)

                complaint.company_relation = \
                    dict(data.COMPANY_RELATION_CHOICES)[int(form.cleaned_data['company_relation'])]

                if int(form.cleaned_data['company_relation']) == data.OTHER_CHOICE:
                    complaint.company_relation = form.cleaned_data['other_relation']

                complaint.people_complaint = []
                for k, item in request.POST.items():
                    if k.startswith('personcomplaint_set-'):
                        complaint.people_complaint.append(item)
                complaint.save()

                send_email(
                    subject='[GECOLSA] Nueva denuncia desde el portal web',
                    recipients=settings.DEFAULT_EMAIL_COMPLAINT,
                    email_template='email/complaint_email.html',
                    dictionary={'data': complaint},
                    attach=complaint.document.url if complaint.document else None
                )

                messages.success(self.request, 'Envío satisfactorio')
                return HttpResponseRedirect(reverse('requests_complaints'))

            except (ValueError, KeyError):
                messages.error(self.request, 'Revisa los errores del formulario.')
                return self.render_to_response(self.get_context_data(
                    form=form
                ))

        return self.form_invalid(form)
