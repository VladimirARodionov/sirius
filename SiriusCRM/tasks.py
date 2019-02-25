from celery import Celery
from pytg.sender import Sender

from SiriusCRM.models import Appointment

app = Celery('tasks', broker='amqp://localhost')


@app.task
def send_telegram_notification(appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    sender = Sender(host="localhost", port=4458)
    message = "New appointment has been made on date: {} time: {}".format(str(appointment.date), str(appointment.time))
    sender.send_msg('@VladimirARodionov', message)
