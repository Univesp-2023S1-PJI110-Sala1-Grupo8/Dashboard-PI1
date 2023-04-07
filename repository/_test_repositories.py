import datetime
from _database import Database
from model.user_model import User
from model.profile_model import Profile
from model.project_model import Project
from model.feature_model import Feature
from model.category_model import Category
from model.value_objects import ProjectStatus
from model.value_objects import FeatureStatus
from repository.user_repository import UserRepository
from repository.project_repository import ProjectRepository
from repository.feature_repository import FeatureRepository
from repository.category_repository import CategoryRepository
from repository.permission_repository import PermissionRepository

def test_repositories():
    db = Database()
    db.connect()
    db.test()

    # test user repository ---------------------------------------------------------------------------------------------

    print("=== Test User Repository ===")

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

    user_john = User(first_name="Joao", last_name="da Silva",
                     password="joao123", email="joao@email.com", profile=Profile(2, ""))

    user_mary = User(first_name="Maria", last_name="dos Santos",
                     password="maria123", email="maria@email.com", profile=Profile(2, ""))

    # delete john and mary if they already exists
    user_repository.delete_user(user_john.email)
    user_repository.delete_user(user_mary.email)

    user_john = user_repository.insert_user(user_john)
    user_mary = user_repository.insert_user(user_mary)

    users = user_repository.get_all_users()
    for user in users:
        print(user)

    # test project repository ------------------------------------------------------------------------------------------

    print("=== Test Project Repository ===")

    project_user = user_to_update

    new_project = Project(name="New Project", short_name="TST_PROJ",
                      description="A project to test the project repository", percent_done=0,
                      status=ProjectStatus.ACTIVE, owner=project_user)

    project_repository = ProjectRepository(db)

    test_project = project_repository.insert_project(new_project)
    project_repository.delete_project(test_project.id)
    test_project = project_repository.insert_project(new_project)
    print(test_project)

    test_project.name = "Test Project"
    test_project.percent_done = 50
    project_repository.update_project(test_project)
    print(test_project)

    # test category repository -----------------------------------------------------------------------------------------

    print("=== Test Category Repository ===")

    category_repository = CategoryRepository(db)

    category1 = Category(name="Test Category 1 for Test Project")
    category1 = category_repository.insert_category(category1, test_project.id)
    category2 = Category(name="Test Category 2 for Test Project")
    category2 = category_repository.insert_category(category2, test_project.id)

    categories_in_project = category_repository.get_all_categories_in_project(test_project.id)
    if categories_in_project is not None:
        for category in categories_in_project:
            print(category)

    # test feature repository ------------------------------------------------------------------------------------------

    print("=== Test Feature Repository ===")

    feature_repository = FeatureRepository(db)

    feature1_category1 = Feature(name="Test Feature 1", short_name="F1_C1", description="Descricao 1",
                                 estimated_end_date=datetime.datetime(2023, 4, 10), percent_done=10,
                                 status=FeatureStatus.NOT_STARTED)
    feature2_category1 = Feature(name="Test Feature 2", short_name="F2_C1", description="Descricao 2",
                                 estimated_end_date=datetime.datetime(2023, 4, 12), percent_done=20,
                                 status=FeatureStatus.UNDER_CONSTRUCTION)
    feature3_category2 = Feature(name="Test Feature 3", short_name="F3_C2", description="Descricao 3",
                                 estimated_end_date=datetime.datetime(2023, 5, 20), percent_done=20,
                                 status=FeatureStatus.CONSTRUCTED)
    feature4_category2 = Feature(name="Test Feature 4", short_name="F4_C2", description="Descricao 4",
                                 estimated_end_date=datetime.datetime(2023, 5, 30), percent_done=20,
                                 status=FeatureStatus.TESTED)

    inserted_feature1 = feature_repository.insert_feature(feature1_category1, category1.id, test_project.id)
    inserted_feature2 = feature_repository.insert_feature(feature2_category1, category1.id, test_project.id)
    inserted_feature3 = feature_repository.insert_feature(feature3_category2, category2.id, test_project.id)
    inserted_feature4 = feature_repository.insert_feature(feature4_category2, category2.id, test_project.id)

    print(inserted_feature1)
    print(inserted_feature2)
    print(inserted_feature3)
    print(inserted_feature4)

    # test permissions repository --------------------------------------------------------------------------------------

    print("=== Test Permission Repository ===")

    permission_repository = PermissionRepository(db)

    permission_repository.delete_permission(user_john.id, test_project.id)
    permission_repository.delete_permission(user_mary.id, test_project.id)

    permission_repository.insert_permission(user_john.id, test_project.id)
    permission_repository.insert_permission(user_mary.id, test_project.id)

    allowed_users = permission_repository.get_allowed_users_in_project(test_project.id)
    if allowed_users is not None:
        print("Allowed user for Test Project:")
        for user in allowed_users:
            print(user)


if __name__ == '__main__':
    test_repositories()
