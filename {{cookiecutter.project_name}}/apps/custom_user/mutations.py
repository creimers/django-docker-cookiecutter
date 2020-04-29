from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from apps.custom_user.emails import send_activation_email, send_password_reset_email
from apps.custom_user.utils import decode_uid

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
# CONFIRM EMAIL
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

################
# RESET PASSWORD
################


class ResetPasswordInput(graphene.InputObjectType):
    email = graphene.String(required=True)


class ResetPassword(graphene.Mutation):
    """
    Mutation for requesting a password reset email
    """

    class Arguments:
        input = ResetPasswordInput()

    success = graphene.Boolean()

    def mutate(self, info, input):
        email = input.get("email", None)
        if not email:
            raise GraphQLError("Please enter a valid email address.")
        try:
            user = UserModel.objects.get(email=email)
            if user.is_active:
                {% if cookiecutter.celery == 'y' %}
                send_password_reset_email.delay(user.id)
                {% else %}
                send_password_reset_email(user.id)
                {% endif %}
            return ResetPassword(success=True)
        # TODO: WTF!
        except Exception as e:
            return ResetPassword(success=False)


class ResetPasswordConfirmInput(graphene.InputObjectType):
    uid = graphene.String(required=True)
    token = graphene.String(required=True)
    new_password = graphene.String(required=True)
    re_new_password = graphene.String(required=True)


class ResetPasswordConfirm(graphene.Mutation):
    """
    Mutation for reseting your password
    """

    class Arguments:
        input = ResetPasswordConfirmInput()

    success = graphene.Boolean()

    def mutate(self, info, input):
        uid = input.get("uid")
        token = input.get("token")
        new_password = input.get("new_password")
        re_new_password = input.get("re_new_password")

        user, is_valid = validate_new_password(
            uid, token, new_password, re_new_password
        )
        if user and is_valid:
            user.set_password(new_password)
            user.save()
            return ResetPasswordConfirm(success=True)
        else:
            # TODO: better error handling here
            # see djoser for inspiration
            error = "Something went wrong..."
            raise GraphQLError(error)
