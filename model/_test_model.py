from project_model import Project
from profile_model import Profile
from feature_model import Feature
from category_model import Category

from user_model import User


def test_model():
    profile = Profile("admin")
    print(profile)

    blankUser = User()
    print(blankUser)
    someUser = User(first_name="João", last_name="da Silva", email="joaodasilva@gmail.com", profile=Profile("admin"))
    print(someUser)
    anotherUser = User(first_name="Maria", last_name="dos Santos", email="mariadossantos@gmail.com", profile=Profile("convidado"))
    print(anotherUser)

    emptyProject = Project("Empty Project", "EPROJ", "This is an empty project", someUser)
    print(emptyProject)

    # build a sample project with categories and features

    category1 = Category("Protocol")
    category2 = Category("IHM")

    feature1 = Feature("TCP Protocol", "TCPP")
    feature2 = Feature("UDP Protocol", "UDPP")
    feature3 = Feature("ADP Protocol", "ADPP")

    feature4 = Feature("Display")
    feature5 = Feature("Keyboard")

    category1.addFeature(feature1)
    category1.addFeature(feature2)
    category1.addFeature(feature3)
    category2.addFeature(feature4)
    category2.addFeature(feature5)

    sampleProject = Project("Sample Project", "SPROJ", "This is a sample project", someUser)
    sampleProject.addCategory(category1)
    sampleProject.addCategory(category2)
    print(sampleProject)

    # try to insert existing features, nothing must be changed
    sampleProject.addFeatureInCategory(feature1, category1)
    sampleProject.addFeatureInCategory(feature1, category1)
    print(sampleProject)

    # try to remove an existing feature, only one remove must work
    sampleProject.removeFeatureFromCategory(feature1, category1)
    sampleProject.removeFeatureFromCategory(feature1, category1)
    sampleProject.removeFeatureFromCategory(feature1, category1)
    print(sampleProject)


if __name__ == '__main__':
    test_model()
