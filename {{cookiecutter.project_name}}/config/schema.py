from django.contrib.auth import get_user_model
import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from apps.custom_user.mutations import (
    Register,
    ConfirmEmail,
    ResetPassword,
    ResetPasswordConfirm,
)

USER = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = USER
        exclude = ("password", "is_superuser")


class ViewerType(graphene.ObjectType):
    user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        return info.context.user


class RootQuery(graphene.ObjectType):
    viewer = graphene.Field(ViewerType)

    def resolve_viewer(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class Mutation(graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

    # account
    register = Register.Field()
    confirm_email = ConfirmEmail.Field()
    reset_password = ResetPassword.Field()
    reset_password_confirm = ResetPasswordConfirm.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutation)
