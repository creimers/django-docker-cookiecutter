from django.contrib.auth import get_user_model
import pytest

import factory
from faker import Factory as FakerFactory

User = get_user_model()
faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):

    """User factory."""

    class Meta:
        model = User

    email = factory.LazyAttribute(lambda x: faker.email())
