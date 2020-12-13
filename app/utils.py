import time
import json
import hashlib

from io import BytesIO
from PIL import Image

import requests
from requests.exceptions import Timeout

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.validators import validate_email

from premailer import transform
from constance import config
import unicodecsv

from app.tasks import task_send_email
from common.models import WsLog


def get_base_url():
    """ Return site's base URL.
    """
    return 'https://{0}'.format(
        Site.objects.get_current().domain,
    )


def render_to_email(
        template_name,
        dictionary=None,
        context_instance=None
):
    base_url = get_base_url()

    dictionary.update({
        'base_url': base_url,
        'site_name': Site.objects.get_current().name,
    })
    return transform(render_to_string(
        template_name,
        dictionary,
        context_instance,
    ))


def send_email(subject, recipients, email_template, dictionary, from_addr=None,
               bcc_mails=None, attach=None):
    if from_addr is None:
        from_addr = settings.DEFAULT_FROM_EMAIL
    msg = render_to_email(email_template, dictionary)
    task_send_email.delay(
        recipients,
        subject,
        msg,
        from_addr,
        bcc_mails,
        attach
    )


def unique_case_insensitive(obj, field):
    query_dict = {
        '{0}__icontains'.format(field): getattr(obj, field)
    }
    others = type(obj).objects.filter(**query_dict).exclude(id=obj.id)
    if others.exists():
        raise ValidationError('{0} ya estaba presente'.format(others.first()))


def loadfile(filename, delimiter=","):
    """Loads the file named as filename (a csv one), separated with delimiter
    returns an array with the contents of the file.
    """
    csv_file = open(filename, "rU")
    reader = unicodecsv.reader(csv_file, encoding='utf-8', delimiter=delimiter)
    answer = []
    for row in reader:
        newrow = []
        for item in row:
            newrow.append(item.strip())
        answer.append(newrow)

    csv_file.close()
    return answer


def get_webservice(endpoint, request_data, category, timeout=5, headers=None):
    """Invokes a webservice and logs the result of the invocation, returns a
    pair of data, the first one is the errors, and the second the actual data,
    which is None if we have errors.
    endpoint: The url of the service
    request_data: json of data to post
    categoy: a title to aggregate
    returns a json if succeeds, None otherwise
    """
    if headers is None:
        headers = {'Content-type': 'application/json'}

    try:
        answer = requests.post(endpoint, headers=headers, data=json.dumps(
            request_data
        ), timeout=timeout)
        if not answer.ok:
            # There was an error, notify administrator
            task_send_email.delay(
                [
                    email.strip()
                    for email in config.EMAIL_GECOLSA_WSDL.split(',')
                ],
                '[{0} - {1} Webservice con errores'.format(
                    Site.objects.get_current().name,
                    category,
                ),
                'Webservice con errores {0}{1}'.format(
                    Site.objects.get_current().domain,
                    reverse('admin:common_wslog_changelist'),
                )
            )
            WsLog.objects.create(
                endpoint=endpoint,
                status_code=answer.status_code,
                request_data=json.dumps(request_data),
                answer_data='',
                ellapsed_time=answer.elapsed.total_seconds(),
                category=category,
            )
            return 'Fallo de comunicación', None
        result = json.loads(answer.text)
        WsLog.objects.create(
            endpoint=endpoint,
            status_code=answer.status_code,
            request_data=json.dumps(request_data),
            answer_data=answer.text,
            ellapsed_time=answer.elapsed.total_seconds(),
            category=category,
        )
        return None, result
    except Timeout:
        task_send_email.delay(
            [email.strip() for email in config.EMAIL_GECOLSA_WSDL.split(',')],
            '[Gecolsa] Webservice {0} lento'.format(
                category,
            ),
            'El Webservice toma más de {0} segundos {1}{2}'.format(
                timeout,
                Site.objects.get_current().domain,
                reverse('admin:common_wslog_changelist'),
            )
        )
        WsLog.objects.create(
            endpoint=endpoint,
            status_code=408,
            request_data=json.dumps(request_data),
            answer_data='Timeout {0} seconds'.format(timeout),
            ellapsed_time=timeout,
            category=category,
        )
        return 'El Webservice toma más de {0} segundos'.format(timeout), None


def log_webservice(request, start_time, request_data, category,
                   status_code=200, answer=''):
    endpoint = '{0}{1}'.format(get_base_url(), request.path)
    wslog = WsLog.objects.create(
        endpoint=endpoint,
        status_code=status_code,
        request_data=request_data,
        answer_data=answer,
        ellapsed_time=time.time() - start_time,
        category=category,
    )

    return wslog


def str_uid(incoming):
    return '{0}'.format(
        int(hashlib.md5(incoming.encode('utf-8')).hexdigest(), 16)
    )[:22]


def validate_emails(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def get_test_image(size=None, format_image='PNG'):
    """ Returns an image for running tests
    """
    io_var = BytesIO()
    color = (255, 0, 0, 0)

    if size is None:
        size = (10, 10)

    image = Image.new('RGBA', size, color)
    image.save(io_var, format=format_image)
    image_file = InMemoryUploadedFile(
        io_var,
        None,
        'test.{}'.format(format_image.lower()),
        format_image.lower(),
        None,
        None,
    )
    image_file.seek(0)

    return image_file
