from io import BytesIO
import xlwt

from django.core.mail import EmailMessage
from django.utils.timezone import now

from celery import task

from cms.models import SatelliteMonitoringContact


@task()
def task_send_satellite_report(email):
    subscriptions = SatelliteMonitoringContact.objects.all()
    output = BytesIO()

    date_format = '%Y-%m-%d'

    xls = xlwt.Workbook()
    sheet = xls.add_sheet('Reporte inscripciones satelital')

    sheet.write(0, 0, 'Nombre Completo')
    sheet.write(0, 1, 'Empresa')
    sheet.write(0, 3, 'Correo electrónico')
    sheet.write(0, 4, 'Teléfono')
    sheet.write(0, 5, 'Dirección')
    sheet.write(0, 6, 'Máquinas que desea monitorear')
    sheet.write(0, 7, 'Fecha')

    row = 1
    for subscription in subscriptions:
        localdate = subscription.created_at.strftime(date_format)
        sheet.write(row, 0, '{0}'.format(subscription.name))
        sheet.write(row, 1, '{0}'.format(subscription.company))
        sheet.write(row, 3, '{0}'.format(subscription.email))
        sheet.write(row, 4, '{0}'.format(subscription.phone))
        sheet.write(row, 5, '{0}'.format(subscription.address))
        sheet.write(row, 6, '{0}'.format(subscription.machine))
        sheet.write(row, 7, localdate)
        row += 1

    xls.save(output)
    output.seek(0)

    email_message = EmailMessage(
        '[Gecolsa] Reporte de solicitud satelital',
        'Cantidad de inscripciones: {0}'.format(subscriptions.count()),
        to=email,
    )

    email_message.content_subtype = 'html'
    email_message.attach(
        'reporte-satelital-{0}.xls'.format(now().strftime(
            "%Y-%m-%d-%H:%M:%S"
        )),
        output.getvalue(),
        'application/ms-excel'
    )
    email_message.send()

    return 'Satellite Subscription report sent to: {0}'.format(','.join(
        email
    ))
