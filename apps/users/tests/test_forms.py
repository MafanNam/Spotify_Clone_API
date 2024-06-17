from django.contrib.auth import get_user_model
from django.test import TestCase

from ..forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserChangeFormTest(TestCase):
    def test_valid_user_change_form(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="Pass1234",
            display_name="test",
            type_profile="user",
            gender="male",
            country="UA",
        )
        form_data = {
            "email": "changed2@example.com",
            "display_name": "test",
            "gender": "male",
            "type_profile": "user",
            "country": "UA",
            "date_joined": user.date_joined,
        }
        form = UserChangeForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_change_form(self):
        user = User.objects.create_user(email="test@example.com", password="Pass1234")
        form_data = {"email": "test@example.com"}  # Trying to change email to an existing one
        form = UserChangeForm(instance=user, data=form_data)
        self.assertFalse(form.is_valid())


class UserCreationFormTest(TestCase):
    def test_valid_user_creation_form(self):
        form_data = {
            "email": "newuser@example.com",
            "password1": "Pass12345",
            "password2": "Pass12345",
            "display_name": "test",
            "gender": "male",
            "type_profile": "user",
            "country": "UA",
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_creation_form(self):
        User.objects.create_user(email="existing@example.com", password="Pass1234")
        form_data = {
            "email": "existing@example.com",
            "password1": "Pass123",
            "password2": "Pass123",
            "display_name": 0,
            "gender": "male",
            "type_profile": "NOT",
            "country": "NOT COUNTRY",
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
