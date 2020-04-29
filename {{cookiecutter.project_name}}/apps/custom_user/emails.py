{%- if cookiecutter.celery == 'y' %}
from celery import shared_task
{%- endif %}

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string

UserModel = get_user_model()


def encode_uid(pk: int):
    return force_text(urlsafe_base64_encode(force_bytes(pk)))


{% if cookiecutter.celery == 'y' %}
@shared_task {% endif %}
def send_activation_email(user_id, request):
    """
    send an email to the user containing an activation link
    """
    user = UserModel.get(id=user_id)
    site = get_current_site(request)
    domain = getattr(settings, "DOMAIN", "") or site.domain

    context = {}
    uid = encode_uid(user.pk)
    token = default_token_generator.make_token(user)
    context["protocol"] = settings.PROTOCOL
    context["domain"] = domain
    context["url"] = f"confirm-email?uid={uid}&token={token}"

    # TODO: make configurable
    subject = "Verify your email."

    body = render_to_string("custom_user/activation.txt", context)

    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email],)
    email.send()


{% if cookiecutter.celery == 'y' %}
@shared_task {% endif %}
def send_password_reset_email(user_id, request):
    """
    send an email to the to reset the password
    """
    user = UserModel.get(id=user_id)
    site = get_current_site(request
    )
    domain = getattr(settings, "DOMAIN", "") or site.domain

    context = {}
    uid = encode_uid(user.pk)
    token = default_token_generator.make_token(user)
    context["protocol"] = settings.PROTOCOL
    context["domain"] = domain
    context["url"] = f"set-new-password?uid={uid}&token={token}"

    # TODO: make configurable
    subject = "Reset your password."

    body = render_to_string("custom_user/reset-password.txt", context)

    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email],)
    email.send()
