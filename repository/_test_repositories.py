from _database import Database
from model.user_model import User
from model.profile_model import Profile
from user_repository import UserRepository


def test_repositories():
    db = Database()
    db.connect()
    db.test()

    # test user repository
    user_repository = UserRepository(db)

    user_email = "testuser@gmail.com"

    deleted = user_repository.delete_user(user_email)
    print('Test User {}'.format("deleted." if deleted else "not deleted."))

    new_user = User(first_name="Test Insert User First Name", last_name="Last Name",
                    password="test123", email=user_email, profile=Profile(2, ""))

    inserted_user = user_repository.insert_user(new_user)

    if inserted_user is not None:
        print('Inserted user:', inserted_user)
    else:
        print("Error while inserting a new user.")

    user_to_update = inserted_user
    user_to_update.first_name = "Test Update User First Name"
    updated_user = user_repository.update_user(user_to_update)
    if updated_user is not None:
        print('Updated user:', updated_user)
    else:
        print("Error while inserting a new user.")


    users = user_repository.get_all_users()
    print("=== All Users ===")
    for user in users:
        print(user)


if __name__ == '__main__':
    test_repositories()
