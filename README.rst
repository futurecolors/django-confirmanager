Simple email confirmation application for django 1.4. Forked from `django-email-confirmation`_

Install
=======

Add ``'confirmanager'`` to your ``INSTALLED_APPS``::

    # settings.py
    INSTALLED_APPS = (
        ...
        'confirmanager',
        ...
    )

Add application urs to your urlconf. Example::

    # urls.py
    urlpatterns += patterns('',
        (r'', include('confirmanager.urls')),
    )

Requires ``django.contrib.sites`` to get absolute url and and user model to save email.

Description
===========

    TBD, meanwhile you can read source.

Limitations
~~~~~~~~~~~

    - one email per user
    - emails are stored in user model
    - emails are sent via django-templated-email (templates/confirmanager/confirmation.html)

Settings
========

* EMAIL_CONFIRMATION_EXPIRES (default 3)
* EMAIL_CONFIRM_REDIRECT_URL
* EMAIL_CONFIRM_LOGIN_URL
* EMAIL_CONFIRM_MANAGER

Signals
=======

* email_confirmed

TODO
====

Make evertything easily overridable (docs for manager, template)
django-appconf

.. _django-email-confirmation: https://github.com/Gidsy/django-email-confirmation