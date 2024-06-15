from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreatePasswordRetypeSerializer(CountryFieldMixin, UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("id", "email", "display_name", "gender", "country", "image", "password")


class CustomUserSerializer(CountryFieldMixin, UserSerializer):
    type_profile = serializers.CharField(source="get_type_profile_display", read_only=True)
    gender = serializers.CharField(source="get_gender_display", read_only=True)
    country = CountryField(name_only=True)
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "display_name",
            "gender",
            "country",
            "image",
            "type_profile",
            "is_premium",
            "followers_count",
        )
        read_only_fields = ("email", "type_profile", "is_premium")


class ShortCustomUserSerializer(CustomUserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "display_name", "type_profile", "image", "is_premium")
