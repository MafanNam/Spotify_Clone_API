from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = [
        "id",
        "email",
        "display_name",
        "gender",
        "type_profile",
        "is_premium",
        "is_staff",
        "is_active",
    ]

    list_editable = ["is_active", "is_premium"]

    list_display_links = ["id", "email"]

    list_filter = ["email", "type_profile", "gender", "is_premium", "is_staff", "is_active"]

    fieldsets = (
        (_("Personal Info"), {"fields": ("display_name", "country", "gender", "type_profile")}),
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
        (_("Other Info"), {"fields": ("image", "followers", "is_premium", "is_spam_email")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "display_name",
                    "gender",
                    "country",
                    "type_profile",
                    "image",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ["email", "display_name"]
