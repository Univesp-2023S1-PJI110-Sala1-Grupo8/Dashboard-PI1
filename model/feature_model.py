from base_entity_model import Entity
from value_objects import FeatureStatus

class Feature(Entity):
    """
    A class to represent the feature entity.
    """
    name = ""
    short_name = ""
    description = ""
    percent_done = 0.0
    estimated_end_date = None
    status = FeatureStatus.NOT_STARTED

    def __init__(self, name, short_name="", description=""):
        """Constructor with arguments."""
        self.name = name
        self.short_name = short_name
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, Feature):
            return False
        return self.__str__() == other.__str__()

    def __str__(self):
        """User string."""
        return "Feature({0} = {1} | {2}, Percent: {3}, EndDate: {4}, Status: {5})"\
            .format(self.id, self.short_name, self.name, self.percent_done, self.estimated_end_date, self.status)

    def __repr__(self):
        """User representation."""
        return "Project(id={0},shortName='{1}',name='{2}',percentDone='{3}',endDate={4},status={5})'"\
            .format(self.id, self.short_name, self.name, self.percent_done, self.estimated_end_date, self.status)
