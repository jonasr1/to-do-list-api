
from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user_valid = User.objects.create_user(username='João', password='João123')
        
    def test_password_is_hashed(self):
        self.assertNotEqual(self.user_valid.password, 'João123') # Verifica se a senha armazenada não é igual à senha original
        self.assertTrue(self.user_valid.check_password('João123')) # Verifica se a senha fornecida ao método de verificação corresponde à senha correta após hash
    
    def test_create_user_without_username(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', password='1234')

    def test_create_user_without_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='Maria', password='')
