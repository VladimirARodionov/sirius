from celery import Celery
from pytg.sender import Sender

from SiriusCRM.models import Appointment

app = Celery('tasks', broker='amqp://localhost')


@app.task
def send_telegram_notification(appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    sender = Sender(host="localhost", port=4458)
    sender.send_msg('@VladimirARodionov',
                    'New appointment has been made on date: ' + appointment.date + ' time: ' + appointment.time)
