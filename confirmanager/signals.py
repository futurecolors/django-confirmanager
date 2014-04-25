# coding: utf-8
from django.dispatch import Signal


email_confirmed = Signal(providing_args=["email", "previous_email"])
