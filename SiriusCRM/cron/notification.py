from django_cron import CronJobBase, Schedule

from Sirius.settings import LEAD_LINK, APPOINTMENT_LINK
from SiriusCRM.models import Appointment, Lead
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from SiriusCRM.tasks import send_telegram_notification, send_email_notification


class NotificationJob(CronJobBase):
    RUN_EVERY_MINS = 30 # every 30 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'SiriusCRM.cron.notification.NotificationJob'    # a unique code

    def do(self):
        date = datetime.now()
        appointments = Appointment.objects.filter(date=date)
        for appointment in appointments:
            appointment_date = datetime.combine(appointment.date, appointment.time)
            delta = appointment_date - date
            minutes = (delta.total_seconds() % 3600) // 60
            hours = (delta.total_seconds() / 3600)
            if 30 > minutes >= 0 and 1 > hours >= 0:
                self.send_notification(appointment)
        leads = Lead.objects.filter(action_date__lt=(date + timedelta(days=1)), action_time__isnull=False)
        for lead in leads:
            lead_date = datetime.combine(lead.action_date, lead.action_time)
            delta = lead_date - date
            minutes = (delta.total_seconds() % 3600) // 60
            hours = (delta.total_seconds() / 3600)
            if 30 > minutes >= 0 and 1 > hours >= 0:
                self.send_lead_notification(lead)


    def send_notification(self, appointment):
        message = _('You have an appointment.') + '\n' + \
        _('Date: %(date)s') % {'date': str(appointment.date)} + '\n' + \
        _('Time: %(time)s') % {'time': str(appointment.time)} + '\n' + \
        _('Contact name: %(contact_name)s') % {'contact_name': str(appointment.contact.first_name) + " " + str(appointment.contact.last_name)} + '\n' + \
        _('Contact email: %(contact_email)s') % {'contact_email': str(appointment.contact.email)} + '\n' + \
        _('Contact mobile: %(contact_mobile)s') % {'contact_mobile': str(appointment.contact.mobile)} + '\n' + \
        _('Diagnos: %(diagnos)s') % {'diagnos': str(appointment.comment)} + '\n' + \
        _('Link: %(link)s') % {'link': APPOINTMENT_LINK % {'id': appointment.id}}
        if appointment.consultant.telegram:
            send_telegram_notification.delay(appointment.consultant.get_telegram_username(), message)
        if appointment.consultant.email:
            send_email_notification.delay(appointment.consultant.email, 'no-reply@server.raevskyschool.ru',
                                          _('[Zdravniza] appointment notification (%(date)s %(time)s)') % {'date': str(appointment.date), 'time': str(appointment.time)}, message)
        if appointment.contact.email:
            send_email_notification.delay(appointment.contact.email, 'no-reply@server.raevskyschool.ru',
                                      _('[Zdravniza] appointment notification (%(date)s %(time)s)') % {'date': str(appointment.date), 'time': str(appointment.time)}, message)

    def send_lead_notification(self, lead):
        message = _('You have a lead action.') + '\n' + \
        _('Date: %(date)s') % {'date': str(lead.action_date)} + '\n' + \
        _('Time: %(time)s') % {'time': str(lead.action_time)} + '\n' + \
        _('Lead name: %(lead_name)s') % {'lead_name': str(lead.first_name) + " " + str(lead.last_name)} + '\n' + \
        _('Lead email: %(lead_email)s') % {'lead_email': str(lead.email)} + '\n' + \
        _('Lead mobile: %(lead_mobile)s') % {'lead_mobile': str(lead.mobile)} + '\n' + \
        _('Action: %(action)s') % {'action': str(lead.action)} + '\n' + \
        _('Link: %(link)s') % {'link': LEAD_LINK % {'id': lead.id}}
        if lead.consultant.telegram:
            send_telegram_notification.delay(lead.consultant.get_telegram_username(), message)
        if lead.consultant.email:
            send_email_notification.delay(lead.consultant.email, 'no-reply@server.raevskyschool.ru',
                                          _('[CRM] lead action notification (%(date)s %(time)s)') % {'date': str(lead.action_date), 'time': str(lead.action_time)}, message)
