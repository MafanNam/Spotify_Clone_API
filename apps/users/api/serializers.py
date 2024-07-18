from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreatePasswordRetypeSerializer(CountryFieldMixin, UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("id", "email", "display_name", "gender", "country", "type_profile", "image", "password")


class CustomUserSerializer(CountryFieldMixin, UserSerializer):
    type_profile = serializers.CharField(source="get_type_profile_display", read_only=True)
    gender = serializers.CharField(source="get_gender_display", read_only=True)
    country = CountryField(name_only=True)
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
    playlists_count = serializers.IntegerField(source="playlists.count", read_only=True)
    artist_slug = serializers.CharField(source="artist.slug", read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "display_name",
            "gender",
            "country",
            "image",
            "color",
            "type_profile",
            "artist_slug",
            "is_premium",
            "followers_count",
            "following_count",
            "playlists_count",
        )
        read_only_fields = ("email", "type_profile", "is_premium", "color")


class CustomUserUpdateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "display_name",
            "gender",
            "type_profile",
            "country",
            "is_premium",
        )
        read_only_fields = ("email", "type_profile", "is_premium")


class ShortCustomUserSerializer(CustomUserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "display_name", "type_profile", "artist_slug", "image", "followers_count", "is_premium")


class UpdateUserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("image",)
