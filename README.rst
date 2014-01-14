Simple email confirmation application for django 1.4. Forked from `django-email-confirmation`_

.. image:: https://travis-ci.org/futurecolors/django-confirmanager.png?branch=master
    :target: https://travis-ci.org/futurecolors/django-confirmanager

.. image:: https://coveralls.io/repos/futurecolors/django-confirmanager/badge.png?branch=master
    :target: https://coveralls.io/r/futurecolors/django-confirmanager/


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

* CONFIRMANAGER_EXPIRES (default 3) - how long links for email confirmation live
* CONFIRMANAGER_REDIRECT_URL - where to redirect after email is confirmed
* CONFIRMANAGER_LOGIN_URL - where to redirect if user is not authenticated
* CONFIRMANAGER_GET_DOMAIN - override default django.contrib.sites behavior to get current domain
* CONFIRMANAGER_UNIQUE_EMAILS (defaut True) - extra check for unique emails

Signals
=======

* email_confirmed

TODO
====

* Make evertything easily overridable (docs for manager, template)
* django-appconf
* Django 1.5

.. _django-email-confirmation: https://github.com/Gidsy/django-email-confirmation
