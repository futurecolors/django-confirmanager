# coding: utf-8
""" From mock-django
    https://github.com/dcramer/mock-django/blob/master/mock_django/signals.py """
import contextlib
import mock


def get_class(class_string):
    """
    Convert a string version of a function name to the callable object.
    """
    try:
        mod_name, class_name = get_mod_func(class_string)
        if class_name != '':
            cls = getattr(__import__(mod_name, {}, {}, ['']), class_name)
            return cls
    except (ImportError, AttributeError):
        pass
    raise ImportError('Failed to import %s' % class_string)


def get_mod_func(class_string):
    """
    Converts 'django.views.news.stories.story_detail' to
    ('django.views.news.stories', 'story_detail')

    Taken from django.core.urlresolvers
    """
    try:
        dot = class_string.rindex('.')
    except ValueError:
        return class_string, ''
    return class_string[:dot], class_string[dot + 1:]


@contextlib.contextmanager
def mock_signal_receiver(signal, wraps=None, **kwargs):
    """
    Temporarily attaches a receiver to the provided ``signal`` within the scope
    of the context manager.

    The mocked receiver is returned as the ``as`` target of the ``with``
    statement.

    To have the mocked receiver wrap a callable, pass the callable as the
    ``wraps`` keyword argument. All other keyword arguments provided are passed
    through to the signal's ``connect`` method.

    >>> with mock_signal_receiver(post_save, sender=Model) as receiver:
    >>>     Model.objects.create()
    >>>     assert receiver.call_count = 1
    """
    if wraps is None:
        wraps = lambda *args, **kwargs: None

    receiver = mock.Mock(wraps=wraps)
    signal.connect(receiver, **kwargs)
    yield receiver
    signal.disconnect(receiver)