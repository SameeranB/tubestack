from users_module.models import User
from users_module.tests.test_setup import TestModelSetup


class TestModels(TestModelSetup):

    def test_user_model(self) -> None:
        """
        Testing User's model with the following
        1. User is_owner testing
        2. Incomplete User information
        """

        self.assertEqual(User.objects.all().count(), 2)
        self.assertTrue(User.is_owner(self.user1, self.user1))
        self.assertFalse(User.is_owner(self.user1, self.user2))
        self.assertTrue(User.is_owner(self.user2, self.user2))
        self.assertFalse(User.is_owner(self.user2, self.user1))

        # Testing pushing incomplete data of the user
        try:
            self.incorrect_user = User.objects.create(email="test@gmail.com")
        except:
            pass
        try:
            self.incorrect_user2 = User.objects.create(email="test5@gmail.com",
                                                       hobbies="testing321312")
        except:
            pass

        self.assertTrue(User.objects.all().count(), 0)
