from typing import Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

UserModel = get_user_model()


def decode_uid(pk):
    return force_text(urlsafe_base64_decode(pk))


def validate_new_password(
    uid: str, token: str, new_password: str, re_new_password: str
) -> Tuple[UserModel, bool]:
    try:
        uid = decode_uid(uid)
        user = UserModel.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            return None, False
        if new_password == re_new_password:
            return user, True
        return user, False
    except:
        return None, False
