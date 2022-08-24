from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from .models import *


class AppTokenGenerator(PasswordResetTokenGenerator):
    """ Token for verification cod """

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()


def get_mail(request):
    user_id = Customer.objects.filter(user=request.user)
    mails = user_id.email
    for mail in mails:
        list_mail = [mail, ]
        return list_mail


user_mail = get_mail
