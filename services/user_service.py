import hashlib
import random
import string
from model.user_model import User
from model.profile_model import Profile
from model.value_objects import UserProfile
from repository.user_repository import UserRepository

class UserService:
    """
    Business logic and entity access related to users.
    """

    def __init__(self, database):
        self.user_repository = UserRepository(database)

    def encode_user_password(self, password_to_encode):
        return hashlib.md5(password_to_encode.encode()).hexdigest()

    def add_new_user(self, user):
        user.profile = Profile(2, "Guest") # default guest profile is assigned to the user, admin may change
        user.password = self.encode_user_password(user.password)
        return self.user_repository.insert_user(user)

    def change_user_data(self, user):
        return self.user_repository.update_user(user)

    def remove_user(self, user):
        return self.user_repository.delete_user(user.email)

    def reset_password(self, user):
        generated_password = ''.join(random.choices(string.ascii_lowercase, k=8))
        user.password = self.encode_user_password(generated_password)
        self.user_repository.update_user(user)
        print("=== Password Reset === User: {}, Pass:{}".format(user.email, generated_password))
        return generated_password

    def change_user_password(self, user, new_password):
        user.password = self.encode_user_password(new_password)
        self.user_repository.update_user(user)
        return True

    def change_user_profile(self, user, new_profile):
        user.profile = new_profile
        return self.user_repository.update_user(user)

    def authenticate(self, email, password):
        try:
            encoded_password = self.encode_user_password(password)
            user = self.user_repository.find_user_by_email(email)
            if user is not None and user.password == encoded_password:
                return user
        except Exception:
            print("Fail while trying to authenticate user '{}!'".format(email))
        return None