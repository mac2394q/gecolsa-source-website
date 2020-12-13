import urllib.request

from django.core.mail import EmailMessage
from django.conf import settings

from celery import task
from premailer import transform


@task()
def task_send_email(email, subject, message, from_addr=None, bcc_mails=None, attach=None):
    """Send an email to list email. The email argument must
    be a list of emails.
    """
    if from_addr is None:
        from_addr = settings.DEFAULT_FROM_EMAIL

    # We have to import here, otherwise it breaks the module.
    from app.utils import get_base_url

    email_message = EmailMessage(
        subject=subject,
        body=transform(message, base_url=get_base_url()),
        from_email=from_addr,
        to=email,
        bcc=bcc_mails or [],
        headers={'Reply-To': from_addr},
    )
    email_message.content_subtype = 'html'

    if attach:
        with urllib.request.urlopen('{}{}'.format(get_base_url(), attach)) as response:
            email_message.attach(
                attach.split('/')[-1:][0],
                response.read(),
            )

    email_message.send()

    return 'Sent email to: {0}'.format(','.join(email))


@task()
def task_update_index():
    """Updates each 15 minutes the index
    """
    from haystack.management.commands import update_index

    update_index.Command().handle(age=1)

    return 'Index Updated'
