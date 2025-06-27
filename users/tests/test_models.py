
from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user_valid = User.objects.create_user(username="João", password="João123")

    def test_password_is_hashed(self) -> None:
        self.assertNotEqual(self.user_valid.password, "João123") # Verifica se a senha armazenada não é igual à senha original  # noqa: E501
        self.assertTrue(self.user_valid.check_password("João123")) # Verifica se a senha fornecida ao método de verificação corresponde à senha correta após hash  # noqa: E501

    def test_create_user_without_username(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", password="1234")

    def test_create_user_without_password(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(username="Maria", password="")
