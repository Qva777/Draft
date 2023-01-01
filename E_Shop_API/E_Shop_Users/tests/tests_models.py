from .settings_module import *
from django.test import TestCase
from E_Shop_API.E_Shop_Users.models import Clients

django.setup()  # DJANGO_SETTINGS_MODULE


class ClientsModelTest(TestCase):
    """ Test cases for the Clients model """

    def tearDown(self):
        Clients.objects.all().delete()

    def test_create_user(self):
        """ Create a new user and check if all fields are correct """
        user = Clients.objects.create_user(
            username="Test",
            first_name="Test_Name",
            last_name="Test_Surname",
            email="test+1@test.com",
            password="ValidPasswordWith1",
            birth_date="1990-01-01"
        )
        self.assertEqual(user.username, "Test")
        self.assertEqual(user.first_name, "Test_Name")
        self.assertEqual(user.last_name, "Test_Surname")
        self.assertEqual(user.email, "test+1@test.com")
        self.assertTrue(user.check_password("ValidPasswordWith1"))
        self.assertEqual(str(user.birth_date), "1990-01-01")
        self.assertFalse(user.disabled)

    def test_create_superuser(self):
        """ Test creating a new superuser """
        superuser = Clients.objects.create_superuser(
            first_name="Super",
            last_name="User",
            email="super.user@example.com",
            username="superuser",
            password="ValidPasswordWith1Capital",
            birth_date="1990-01-01"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
