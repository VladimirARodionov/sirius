from django_cron import CronJobBase, Schedule

from SiriusCRM.models import Appointment
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from SiriusCRM.tasks import send_telegram_notification, send_email_notification


class NotificationJob(CronJobBase):
    RUN_EVERY_MINS = 30 # every 30 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'SiriusCRM.notification_job'    # a unique code

    def do(self):
        date = datetime.now()
        appointments = Appointment.objects.filter(date=date)
        for appointment in appointments:
            appointment_date = datetime.combine(appointment.date, appointment.time)
            delta = appointment_date - date
            minutes = (delta.total_seconds() % 3600) // 60
            hours = (delta.total_seconds() % 3600)
            if 30 > minutes > 0 and hours == 0:
                self.send_notification(appointment)

    def send_notification(self, appointment):
        message = _(
            'You have an appointment.\nDate: %(date)s\nTime: %(time)s\nContact name: %(contact_name)s\nContact email: %(contact_email)s\nContact mobile: %(contact_mobile)s\nDiagnos: %(diagnos)s') % {
                      'date': str(appointment.date), 'time': str(appointment.time),
                      'contact_name': str(appointment.contact.first_name) + " " + str(appointment.contact.last_name),
                      'contact_email': str(appointment.contact.email),
                      'contact_mobile': str(appointment.contact.mobile), 'diagnos': str(appointment.comment)}
        if appointment.consultant.telegram:
            send_telegram_notification.delay(appointment.consultant.get_telegram_username(), message)
        if appointment.consultant.email:
            send_email_notification.delay(appointment.consultant.email, 'no-reply@server.raevskyschool.ru',
                                          _('[Zdravniza] appointment notification (%(date)s %(time)s)') % {'date': str(appointment.date), 'time': str(appointment.time)}, message)
        send_email_notification.delay(appointment.contact.email, 'no-reply@server.raevskyschool.ru',
                                      _('[Zdravniza] appointment notification (%(date)s %(time)s)') % {'date': str(appointment.date), 'time': str(appointment.time)}, message)
