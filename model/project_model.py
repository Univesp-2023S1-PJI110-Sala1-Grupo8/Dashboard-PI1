from base_entity_model import Entity
from value_objects import ProjectStatus


class Project(Entity):
    """
    A class to represent the project entity.
    """
    name = ""
    short_name = ""
    description = ""
    percent_done = 0.0
    status = ProjectStatus.ACTIVE
    owner = None
    allowed_users = []
    feature_categories = []

    def __init__(self, name, short_name="", description="", owner=None):
        """Constructor with arguments."""
        self.name = name
        self.short_name = short_name
        self.description = description
        self.owner = owner
        self.allowed_users = []
        self.feature_categories = []

    def __eq__(self, other):
        if not isinstance(other, Project):
            return False
        return self.__str__() == other.__str__()

    def __str__(self):
        """User string."""
        return "Project({0} = {1} | {2}, Percent: {3}, Status: {4}, Owner: {5}, Allowed Users: {6}, Categories: {7}, Features: {8})" \
            .format(self.id, self.short_name, self.name, self.percent_done, self.status,
                    "{0} {1}".format(self.owner.first_name, self.owner.last_name) if self.owner is not None else "?",
                    len(self.allowed_users), len(self.feature_categories), self.countTotalOfFeatures())

    def __repr__(self):
        """User representation."""
        return "Project(id={0},shortName='{1}',name='{2}',percentDone='{3}',status={4},owner={5},allowedUsers={6},categories:{7},features:{8})'" \
            .format(self.id, self.short_name, self.name, self.percent_done, self.status,
                    "{0} {1}".format(self.owner.first_name, self.owner.last_name) if self.owner is not None else "?",
                    len(self.allowed_users), len(self.feature_categories), self.countTotalOfFeatures())

    def addGuestUser(self, user):
        if user is not None:
            self.allowed_users.append(user)

    def removeGuestUser(self, user):
        if user is not None:
            self.allowed_users.remove(user)

    def addCategory(self, category):
        if category is not None:
            self.feature_categories.append(category)

    def removeCategory(self, category):
        if category is not None:
            self.feature_categories.remove(category)

    def findCategory(self, category):
        return next((c for c in self.feature_categories if c == category), None)

    def addFeatureInCategory(self, feature, category):
        if category is not None and feature is not None:
            category_in_list = self.findCategory(category)
            if category_in_list is None:
                category_in_list.features.append(category)

    def removeFeatureFromCategory(self, feature, category):
        if category is not None and feature is not None:
            category_in_list = self.findCategory(category)
            if category_in_list is not None:
                try:
                    category_in_list.features.remove(feature)
                    return True
                except ValueError:
                    return False
        return False

    def countTotalOfFeatures(self):
        return sum([len(c.features) for c in self.feature_categories])
