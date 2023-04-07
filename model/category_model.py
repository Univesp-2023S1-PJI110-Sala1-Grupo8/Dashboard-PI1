from model.base_entity_model import Entity


class Category(Entity):
    """
    A class to represent the feature category.

    Attributes:
        id      The category unique id.
        name    The category name.
    """

    def __init__(self, id=0, name=""):
        super().__init__()
        self.id = id
        self.name = name
        self.features = []

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.__str__() == other.__str__()

    def __str__(self):
        """Profile string."""
        return "Category({0}='{1}', features: {2})".format(self.id, self.name, len(self.features))

    def __repr__(self):
        """Profile representation."""
        return "Category(id={0},name='{1},features:{2})".format(self.id, self.name, len(self.features))

    def find_feature(self, feature):
        return next((f for f in self.features if f.id == f.id and f.name == feature.name), None)

    def add_feature(self, feature):
        if feature is not None and self.find_feature(feature) is None:
            self.features.append(feature)

    def remove_feature(self, feature):
        if feature is not None:
            self.features.remove(feature)
