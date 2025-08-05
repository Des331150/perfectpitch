from django.test import TestCase
from pitch.forms import UserRegistrationForm


class UserRegistrationFormTestCase(TestCase):
    def test_form_with_valid_data(self):
        form_data = {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "password1": "abcdef",
            "password2": "abcdef",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
