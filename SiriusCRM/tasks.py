from celery import Celery
from pytg.sender import Sender

app = Celery('tasks', broker='amqp://localhost')


@app.task
def send_telegram_notification(to, message):
    sender = Sender(host="localhost", port=4458)
    sender.send_msg(to, message)
