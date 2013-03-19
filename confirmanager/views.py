# coding: utf-8
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import View
from django.utils.translation import ugettext as _

from .models import EmailConfirmation, ConfirmationExpired, ConfirmationAlreadyVerified


class ConfirmEmail(View):

    def get(self, request, confirmation_key):
        self.confirmation_key = confirmation_key.lower()
        self.populate_context()

        try:
            confirmation = EmailConfirmation.objects.confirm(confirmation_key)
        except ConfirmationExpired:
            return self.handle_expired()
        except ConfirmationAlreadyVerified:
            return self.handle_already_verified()

        if not confirmation:
            return self.handle_missing_code()
        else:
            return self.handle_ok(confirmation)

    def populate_context(self):
        self.next_url = settings.CONFIRMANAGER_REDIRECT_URL
        self.login_url = settings.CONFIRMANAGER_LOGIN_URL

    def handle_expired(self):
        """ If we can, find a expired email confirmation
            then send it again and return error message
        """
        confirmation = EmailConfirmation.objects.get(confirmation_key=self.confirmation_key)
        EmailConfirmation.objects.send_confirmation(confirmation.email, confirmation.user)
        EmailConfirmation.objects.delete_expired_confirmations()

        messages.warning(self.request, _("Whoops, that link doesn't seem to be working anymore!"))
        messages.success(self.request, _("Don't worry, we have sent you a new email. Please check"
                                         "your email account and use the new confirmation key."))

        if self.request.user.is_authenticated():
            # if user is logged in, we want to show the error message on account page
            return redirect(self.next_url)
        else:
            # otherwise we display the error on the login page, prefill the email
            return redirect("%s?email=%s&next=%s" % (self.login_url,
                                                     confirmation.user.email,
                                                     self.next_url))

    def handle_already_verified(self):
        """ Confirmation was verified but somebody clicked the link again,
            doing nothing, except notification

            TODO: refactor  handle_expired & handle_already_verified
        """
        confirmation = EmailConfirmation.objects.get(confirmation_key=self.confirmation_key)

        messages.warning(self.request, _("Whoops, that link doesn't seem to be working anymore!"))
        if self.request.user.is_authenticated():
            # if user is logged in, we want to show the error message on account page
            return redirect(self.next_url)
        else:
            # otherwise we display the error on the login page, prefill the email
            return redirect("%s?email=%s&next=%s" % (self.login_url,
                                                     confirmation.user.email,
                                                     self.next_url))


    def handle_missing_code(self):
        """ If not then it was the wrong, code. the view takes care of that """
        if self.request.user.is_authenticated():
            # if user is logged in, we want to show the error message on account page
            # we don't want to resend the confirmation since we did not find an expired one
            messages.warning(self.request, _("Whoops, that link doesn't work anymore! Re-send the "
                                             "confirmation email by logging in with the corresponding account."))
            return redirect(self.next_url)
        else:
            # otherwise we display the error on the login page, in this case we can't fill the email
            messages.warning(self.request, _("Whoops, that link doesn't seem to exist!  Please login "
                                             "and re-send the confirmation email."))
            return redirect("%s?next=%s" % (self.login_url, self.next_url))


    def handle_ok(self, confirmation):
        """ The email was confirmed, now it depends if user is logged in
            or not and if it was of a different user
        """
        if self.request.user.is_authenticated():
            if self.request.user == confirmation.user:
                # success, just display message on account page
                messages.success(self.request, _("Thanks a lot, you've successfully confirmed your email address. Have fun!"))
                return redirect(self.next_url)
            else:
                # success, but also display a warning telling the user about the different account
                messages.warning(self.request, _("The email you confirmed does not belong to the account you are signed in with."))
                messages.success(self.request, _("Thanks a lot! You succesfully confirmed the email address."))
                return redirect(self.next_url)
        else:
            # if user is logged out we go to login page and display success message
            messages.success(self.request, _("Thanks a lot! You succesfully confirmed the email address."))
            return redirect("%s?email=%s&next=%s" % (self.login_url, confirmation.email, self.next_url))