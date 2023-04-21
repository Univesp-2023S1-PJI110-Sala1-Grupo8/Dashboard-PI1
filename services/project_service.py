from model.value_objects import ProjectStatus
from repository.project_repository import ProjectRepository
from repository.feature_repository import FeatureRepository
from repository.category_repository import CategoryRepository
from repository.permission_repository import PermissionRepository


class ProjectService:

    def __init__(self, database):
        self.project_repository = ProjectRepository(database)
        self.feature_repository = FeatureRepository(database)
        self.category_repository = CategoryRepository(database)
        self.permission_repository = PermissionRepository(database)

    def add_new_project(self, project):
        return self.project_repository.insert_project(project)

    def change_project_data(self, project):
        self.project_repository.update_project(project)
        return self.load_project_by_id(project.id)

    def remove_project(self, project):
        return self.project_repository.delete_project(project.id)

    def get_all_projects_of_user(self, user):
        return self.project_repository.get_all_projects_of_user(user.id)

    def load_project_by_id(self, project_id):
        project = self.project_repository.find_project_by_id(project_id)
        project.allowed_users = self.permission_repository.get_allowed_users_in_project(project.id)
        project.feature_categories = self.category_repository.get_all_categories_in_project(project.id)
        for category in project.feature_categories:
            category.features = self.feature_repository.get_all_features_in_category(category.id)
        project.count_total_of_features()
        return project

    def activate_project(self, project):
        project.status = ProjectStatus.ACTIVE
        self.project_repository.update_project(project)

    def deactivate_project(self, project):
        project.status = ProjectStatus.INACTIVE
        self.project_repository.update_project(project)

    def add_new_category_to_project(self, new_category, project):
        category = self.category_repository.insert_category(new_category, project.id)
        if category is None:
            raise Exception("Category not added to the project.")
        project.add_category(category)
        return category

    def change_category_data(self, category):
        return self.category_repository.update_category(category)

    def remove_category_from_project(self, category, project):
        self.category_repository.delete_category(category.id)
        project.feature_categories = self.category_repository.get_all_categories_in_project(project.id)
        if project.feature_categories is None:
            raise Exception("Project category list not loaded.")
        return project.feature_categories

    def add_new_feature_category(self, new_feature, category, project):
        feature = self.feature_repository.insert_feature(new_feature, category.id, project.id)
        if feature is None:
            raise Exception("Feature not added to the project.")
        category.add_feature(feature)
        return feature

    def change_feature_data(self, feature):
        return self.feature_repository.update_feature(feature)

    def remove_feature_from_category(self, feature, category, project):
        self.feature_repository.delete_feature(feature.id)
        category.features = self.feature_repository.get_all_features_in_category(category.id)
        if category.features is None:
            raise Exception("Category feature list not loaded.")
        return category.features

    def grant_access_to_user(self, user, project):
        try:
            self.permission_repository.insert_permission(user.id, project.id)
        except:
            return False
        return True

    def revoke_access_from_user(self, user, project):
        try:
            self.permission_repository.delete_permission(user.id, project.id)
        except:
            return False
        return True

    def find_project_by_id(self, project_id):
        return self.project_repository.find_project_by_id(project_id)

    def find_category_by_id(self, category_id):
        return self.category_repository.find_category_by_id(category_id)
