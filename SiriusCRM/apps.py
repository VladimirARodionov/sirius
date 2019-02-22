from django.apps import AppConfig
from pytg.sender import Sender


class SiriuscrmConfig(AppConfig):
    name = 'SiriusCRM'
    sender = Sender("localhost", 4458)
