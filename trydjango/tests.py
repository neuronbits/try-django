import os
from django. conf import settings
from django.contrib.auth.password_validation import validate_password
from django.test import TestCase

class TryDjangoConfigTest (TestCase):
    # https://docs.python.org/3/library/unittest.html
    def test_secret_key_strength(self):
        # settings.SECRET_KEY, settings.DEBUG - get all settings
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
        # self.assertNotEqual(SECRET_KEY,'abc')
        try:
            is_string = validate_password(SECRET_KEY)
        except Exception as e:
            msg = f'Weak Secret Key {e.messages}'
            self.fail(msg)
