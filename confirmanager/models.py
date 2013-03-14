# coding: utf-8
import datetime
from random import random
from hashlib import sha1

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

try:
    from django.contrib.sites.models import Site
except ImportError:
    pass
try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.datetime.now
from templated_email import send_templated_mail

from .signals import email_confirmed
from .utils import get_class


class ConfirmationExpired(Exception):
    pass


class EmailConfirmationManager(models.Manager):

    def confirm(self, confirmation_key):
        try:
            confirmation = self.get(confirmation_key=confirmation_key)
        except self.model.DoesNotExist:
            return None
        if confirmation.is_key_expired:
            raise ConfirmationExpired
        else:
            confirmation.user.email = confirmation.email
            confirmation.user.save()
            confirmation.is_verified = True
            confirmation.save()
            email_confirmed.send(sender=self.model, email=confirmation.email)
            return confirmation

    def last_email_for(self, user):
        confirmations = self.filter(user=user, is_verified=False)
        last_unconfirmed = next((c.email for c in confirmations if not c.is_key_expired), None)
        if last_unconfirmed:
            return last_unconfirmed, False
        else:
            return user.email, True

    def send_confirmation(self, email, user):
        confirmation_key = self.get_confirmation_key(email)
        self.send_email(email, user, confirmation_key)
        return self.create(email=email, user=user, sent_on=now(), confirmation_key=confirmation_key)

    def get_confirmation_key(self, email):
        salt = sha1(str(random())).hexdigest()[:5]
        return sha1(salt + email).hexdigest()

    def get_context(self, confirmation_key, user):
        return {
            'activate_url': self.get_confirmation_url(confirmation_key),
            'site_name': self.get_current_domain(),
            'user': user
        }

    def send_email(self, email, user, confirmation_key):
        return send_templated_mail(recipient_list=[email],
                                   from_email=settings.DEFAULT_FROM_EMAIL,
                                   template_prefix='confirmanager/',
                                   template_suffix='html',
                                   template_name='confirmation',
                                   context=self.get_context(confirmation_key, user))

    def get_current_domain(self):
        return Site.objects.get_current().domain

    def get_confirmation_url(self, confirmation_key):
        relative_path = reverse('confirmation-view', args=[confirmation_key])

        return u"http://%s%s" % (self.get_current_domain(), relative_path)

    def delete_expired_confirmations(self):
        for confirmation in self.all():
            if confirmation.is_key_expired:
                confirmation.delete()


class EmailConfirmation(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', User))
    email = models.EmailField(max_length=254)
    sent_on = models.DateTimeField()
    confirmation_key = models.CharField(max_length=40)
    is_verified = models.BooleanField(default=False)

    objects = get_class(getattr(settings, 'EMAIL_CONFIRM_MANAGER',
                                'confirmanager.models.EmailConfirmationManager'))()

    @property
    def is_key_expired(self):
        confirm_timedelta = datetime.timedelta(days=getattr(settings, 'EMAIL_CONFIRMATION_EXPIRES', 3))
        expiration_date = self.sent_on + confirm_timedelta
        return expiration_date <= now()

    def __unicode__(self):
        return u"for {0}".format(self.email)

    class Meta:
        verbose_name = _("e-mail confirmation")
        verbose_name_plural = _("e-mail confirmations")
        ordering = ('-sent_on',)