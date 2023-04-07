from user_model import User
from project_model import Project
from profile_model import Profile
from feature_model import Feature
from category_model import Category


def test_model():
    profile = Profile("admin")
    print(profile)

    blank_user = User()
    print(blank_user)
    some_user = User(first_name="João", last_name="da Silva", email="joaodasilva@gmail.com", profile=Profile("admin"))
    print(some_user)
    another_user = User(first_name="Maria", last_name="dos Santos", email="mariadossantos@gmail.com", profile=Profile("convidado"))
    print(another_user)

    empty_project = Project("Empty Project", "EPROJ", "This is an empty project", some_user)
    print(empty_project)

    # build a sample project with categories and features

    category1 = Category("Protocol")
    category2 = Category("IHM")

    feature1 = Feature("TCP Protocol", "TCPP")
    feature2 = Feature("UDP Protocol", "UDPP")
    feature3 = Feature("ADP Protocol", "ADPP")

    feature4 = Feature("Display")
    feature5 = Feature("Keyboard")

    category1.add_feature(feature1)
    category1.add_feature(feature2)
    category1.add_feature(feature3)
    category2.add_feature(feature4)
    category2.add_feature(feature5)

    sample_project = Project("Sample Project", "SPROJ", "This is a sample project", some_user)
    sample_project.add_category(category1)
    sample_project.add_category(category2)
    print(sample_project)

    # try to insert existing features, nothing must be changed
    sample_project.add_feature_in_category(feature1, category1)
    sample_project.add_feature_in_category(feature1, category1)
    print(sample_project)

    # try to remove an existing feature, only one remove must work
    sample_project.remove_feature_from_category(feature1, category1)
    sample_project.remove_feature_from_category(feature1, category1)
    sample_project.remove_feature_from_category(feature1, category1)
    print(sample_project)


if __name__ == '__main__':
    test_model()
