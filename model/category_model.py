from base_entity_model import Entity


class Category(Entity):
    """
    A class to represent the feature category.

    Attributes:
        id      The category unique id.
        name    The category name.
    """
    name = ""
    features = []

    def __init__(self, name):
        """Constructor with name."""
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

    def findFeature(self, feature):
        return next((f for f in self.features if f.id == f.id and f.name == feature.name), None)

    def addFeature(self, feature):
        if feature is not None and self.findFeature(feature) is None:
            self.features.append(feature)

    def removeFeature(self, feature):
        if feature is not None:
            self.features.remove(feature)
