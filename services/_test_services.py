from model.user_model import User
from model.profile_model import Profile
from model.project_model import Project
from model.feature_model import Feature
from model.category_model import Category
from model.value_objects import UserProfile
from model.value_objects import FeatureStatus
from repository._database import Database
from services.user_service import UserService
from services.project_service import ProjectService


def print_project(project):
    print(project)
    for category in project.feature_categories:
        print('--- :', category)
        for feature in category.features:
            print('--- --- :', feature)
def test_services():

    db = Database()
    db.connect()

    print("=== Test User Services ===")

    user_services = UserService(db)

    user = User(first_name="Alice", last_name="Service", email="alice@email.com", password="a123")
    user_services.remove_user(user)
    user = user_services.add_new_user(user)

    print("User added by services: {}".format(user))

    # try to authenticate with wrong password
    auth_user = user_services.authenticate("alice@email.com", "321a")
    print("User authenticated. {}".format(auth_user) if auth_user is not None else "User not authenticated.")

    # try to authenticate with right password
    auth_user = user_services.authenticate("alice@email.com", "a123")
    print("User authenticated. {}".format(auth_user) if auth_user is not None else "User not authenticated.")

    # reset user password
    reset_password = user_services.reset_password(user)
    print("Reset Password to:", reset_password)

    # try to authenticate with old right password
    auth_user = user_services.authenticate("alice@email.com", "a123")
    print("User authenticated. {}".format(auth_user) if auth_user is not None else "User not authenticated.")

    # try to authenticate with reset password
    auth_user = user_services.authenticate("alice@email.com", reset_password)
    print("User authenticated. {}".format(auth_user) if auth_user is not None else "User not authenticated.")

    new_password = "alc2023"
    print("Change Password to a new one:", new_password)
    user_services.change_user_password(user, new_password)

    # try to authenticate with reset password
    auth_user = user_services.authenticate("alice@email.com", reset_password)
    print("User authenticated. {}".format(auth_user) if auth_user is not None else "User not authenticated.")

    # try to authenticate with new password
    auth_user = user_services.authenticate("alice@email.com", new_password)
    print("User authenticated. {}".format(auth_user) if auth_user is not None else "User not authenticated.")

    # change user data
    user.last_name = "Last name changed"
    user = user_services.change_user_data(user)
    print(user)

    # change profile
    user.profile = UserProfile.PRODUCT_OWNER
    user = user_services.change_user_data(user)
    print(user)

    print("=== Test Project Services ===")

    # build a sample project with categories and features

    category1 = Category(name="Protocol")
    category2 = Category(name="IHM")

    feature1 = Feature(name="TCP Protocol", short_name="F1")
    feature2 = Feature(name="UDP Protocol", short_name="F2")
    feature3 = Feature(name="ADP Protocol", short_name="F3")

    feature4 = Feature(name="Display", short_name="F4")
    feature5 = Feature(name="Keyboard", short_name="F5")

    category1.add_feature(feature1)
    category1.add_feature(feature2)
    category1.add_feature(feature3)
    category2.add_feature(feature4)
    category2.add_feature(feature5)

    project = Project(name="Project 1", short_name="PROJ1", description="This is a service sample project", owner=user)

    project_service = ProjectService(db)
    project_service.remove_project(project)
    project = project_service.add_new_project(project)
    print(project)

    category1 = project_service.add_new_category_to_project(category1, project)
    print(project)
    category2 = project_service.add_new_category_to_project(category2, project)
    print(project)

    feature1 = project_service.add_new_feature_category(feature1, category1, project)
    print(project)
    feature2 = project_service.add_new_feature_category(feature2, category1, project)
    print(project)
    feature3 = project_service.add_new_feature_category(feature3, category1, project)
    print(project)
    feature4 = project_service.add_new_feature_category(feature4, category2, project)
    print(project)
    feature5 = project_service.add_new_feature_category(feature5, category2, project)
    print(project)

    project = project_service.load_project_by_id(project.id)
    print(project)

    # change project data
    project.percent_done = 50
    project = project_service.change_project_data(project)
    print(project)

    print_project(project)

    project.feature_categories[0].features[0].percent_done = 75
    project_service.change_feature_data(project.feature_categories[0].features[0])

    project.feature_categories[0].features[2].status = FeatureStatus.CANCELED
    project_service.change_feature_data(project.feature_categories[0].features[2])

    p = project_service.load_project_by_id(project.id)
    print_project(p)

    user_martines = User(first_name="Fernando", last_name="Martines",
                     password="123", email="martines", profile=Profile(2, ""))
    user_services.add_new_user(user_martines)

    db.disconnect()


if __name__ == '__main__':
    test_services()
