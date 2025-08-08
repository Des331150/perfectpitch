from django.test import TestCase
from pitch.forms import UserRegistrationForm, UserLoginForm


class UserRegistrationFormTestCase(TestCase):
    def test_form_with_valid_data(self):
        form_data = {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "password1": "hotflame02",
            "password2": "hotflame02",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_missing_fields(self):
        form_data = {
            "name": "",
            "email": "",
            "password1": "hotflame02",
            "password2": "hotflame02",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_password_mismatch(self):
        form_data = {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "password1": "hotflame02",
            "password2": "hotkink99",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserLoginFormTest(TestCase):
    def test_with_valid_form(self):
        form_data = {"email": "arhinfuldesmondpapa@gmail.com", "password": "hotflame02"}

        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
