from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

import pytest

from apps.custom_user.emails import encode_uid

User = get_user_model()


@pytest.mark.django_db
def test_register_mutation_success(client, mailoutbox):
    email = "affe@giraffe.de"
    user_password = "secure123!"
    query = """
    mutation {
      register( input: { email: "%s", password: "%s" })
      {
        success
      }
    }
    """ % (
        email,
        user_password,
    )

    query = "?query=" + query.replace("\n", "").replace(" ", "")
    url = reverse("graphql") + query

    response = client.post(url)
    result = response.json()

    assert not result.get("errors", None)
    assert len(mailoutbox) == 1

    user = User.objects.get(email=email)
    assert user.check_password(user_password)
    assert user.is_active is False


@pytest.mark.django_db
def test_confirm_email_success(client, user_factory, rf):
    user = user_factory.create(is_active=False)
    assert user.is_active is False

    uid = encode_uid(user.pk)
    token = default_token_generator.make_token(user)

    query = """
    mutation {
        confirmEmail( input: { token: "%s", uid: "%s"}) {
            success
        }
    }
    """ % (
        token,
        uid,
    )

    query = "?query=" + query.replace("\n", "").replace(" ", "")
    url = reverse("graphql") + query

    response = client.post(url)
    result = response.json()
    assert not result.get("errors", None)

    user.refresh_from_db()
    assert user.is_active
