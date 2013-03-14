# coding: utf-8
import datetime
import random
import string

from django.contrib.auth.models import User
import factory

from .models import EmailConfirmation


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'username_%s' % n)
    password = factory.PostGenerationMethodCall('set_password', '1234')


class ConfirmationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = EmailConfirmation
    user = factory.SubFactory(UserFactory)
    confirmation_key = factory.LazyAttribute(lambda _: ''.join(random.choice(string.digits) for x in range(10)))
    sent_on = factory.LazyAttribute(lambda _: datetime.datetime.now())

    @factory.post_generation
    def is_expired(self, create, extracted):
        if extracted:
            self.sent_on = datetime.datetime(1985, 11, 5)
            self.save()