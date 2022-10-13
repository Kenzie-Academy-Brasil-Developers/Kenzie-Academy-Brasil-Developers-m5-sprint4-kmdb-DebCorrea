from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from users.models import User


class UsersViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users"

        cls.critic_data = {
            "username": "lucira",
            "email": "lucira@mail.com",
            "birthdate": "1999-09-09",
            "first_name": "Lucira",
            "last_name": "Critica",
            "password": "1234",
            "is_critic": True,
        }

    def test_can_create_user(self):
        """
        Verifica se o usuário é criado propriamente com dados corretos
        """
        response = self.client.post(f"{self.BASE_URL}/register/", self.critic_data)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(User.objects.count(), 1)

    def test_if_password_is_hashed(self):
        """
        Verifica se a senha está sendo hasheada corretamente para permanência no banco
        """
        self.client.post(f"{self.BASE_URL}/register/", self.critic_data)

        user = User.objects.get(id=1)

        self.assertTrue(user.check_password(self.critic_data["password"]))

    def test_returning_keys(self):
        """
        Verifica se o retorno da requisição tem as chaves esperadas
        """
        response = self.client.post(f"{self.BASE_URL}/register/", self.critic_data)

        expected_keys = {
            "id",
            "username",
            "email",
            "birthdate",
            "first_name",
            "last_name",
            "bio",
            "is_critic",
            "updated_at",
            "is_superuser",
        }

        self.assertSetEqual(set(response.data.keys()), expected_keys)

    def test_duplicated_username_and_email_error(self):
        """
        Verifica se propriedades `username` e `email` tem constraint unique
        """
        self.client.post(f"{self.BASE_URL}/register/", self.critic_data)

        response = self.client.post(f"{self.BASE_URL}/register/", self.critic_data)

        self.assertEqual(response.status_code, 400)

        self.assertRaisesMessage(
            ValidationError,
            {
                "username": ["username already exists"],
                "email": ["email already exists"],
            },
        )

    def test_missing_keys_error(self):
        """
        Verifica se requisição retorna erro com chaves faltando no body
        """
        response = self.client.post(f"{self.BASE_URL}/register/", {})

        self.assertEqual(response.status_code, 400)

        self.assertRaisesMessage(
            KeyError,
            {
                "username": ["This field is required."],
                "email": ["This field is required."],
                "birthdate": ["This field is required."],
                "first_name": ["This field is required."],
                "last_name": ["This field is required."],
                "password": ["This field is required."],
            },
        )
