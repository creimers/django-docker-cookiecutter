from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser.utils import decode_uid
import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from apps.custom_user.emails import send_activation_email, send_password_reset_email
# from apps.account.serializers import PasswordResetConfirmRetypeSerializer

UserModel = get_user_model()

##############
# REGISTRATION
##############


class RegisterInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class Register(graphene.Mutation):
    """
    Mutation to register a user
    """

    class Arguments:
        input = RegisterInput()

    success = graphene.Boolean()

    def mutate(self, info, input):
        email = input.get("email")
        password = input.get("password")

        user, created = UserModel.objects.get_or_create(email=email)
        if not created:
            error = "Email address already registered."
            raise GraphQLError(error)
        user.is_active = False
        user.set_password(password)
        user.save()

        {% if cookiecutter.celery == 'y' %}
        send_activation_email.delay(user.id, info.context)
        {% else %}
        send_activation_email(user.id, info.context)
        {% endif %}

        return Register(success=True)

###############
# confirm email
###############


class ConfirmEmailInput(graphene.InputObjectType):
    token = graphene.String(required=True)
    uid = graphene.String(required=True)


class ConfirmEmail(graphene.Mutation):
    """
    Mutation to confirm a user's email address
    """

    class Arguments:
        input = ConfirmEmailInput()

    success = graphene.Boolean()

    def mutate(self, info, input):
        uid = input.get("uid")
        token = input.get("token")
        try:
            uid = decode_uid(uid)
            user = UserModel.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                error = "Activation code invalid. You might have waited too long. Try again with a new activation link."
                raise GraphQLError(error)

            user.is_active = True
            user.save()

            return ConfirmEmail(success=True)

        except UserModel.DoesNotExist:
            error = "Unknown user."
            raise GraphQLError(error)
