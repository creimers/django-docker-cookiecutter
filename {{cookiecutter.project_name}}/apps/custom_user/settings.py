from django.conf import settings
from django.utils.translation import ugettext_lazy as _

CUSTOM_USER_SETTINGS = {
    "app_verbose_name": _("Custom User"),
    "register_proxy_auth_group_model": False,
}

if hasattr(settings, "CUSTOM_USER"):
    CUSTOM_USER_SETTINGS.update(settings.CUSTOM_USER)
