from django.apps import AppConfig
from .settings import CUSTOM_USER_SETTINGS


class CustomUserConfig(AppConfig):
    name = "apps.custom_user"
    verbose_name = CUSTOM_USER_SETTINGS["app_verbose_name"]
