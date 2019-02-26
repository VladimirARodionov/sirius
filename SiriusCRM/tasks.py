from celery import Celery
from django.core.mail import send_mail
from pytg.sender import Sender

app = Celery('tasks', broker='amqp://localhost')


@app.task
def send_telegram_notification(to, message):
    sender = Sender(host="localhost", port=4458)
    sender.send_msg(to, message)


@app.task
def send_email_notification(to_email, from_email, subject, message):
    send_mail(subject, message, from_email, [to_email])