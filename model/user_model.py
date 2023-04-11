from dataclasses import dataclass
from model.base_entity_model import Entity
from model.profile_model import Profile

@dataclass
class User(Entity):
    """
    A class to represent the user entity.
    """

    def __init__(self, id=0, first_name="", last_name="", email="", password="", profile=None):
        super().__init__()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.profile = profile

    def __eq__(self, other):
        if not isinstance(other, Profile):
            return False
        return self.__str__() == other.__str__()

    def __str__(self):
        """User string."""
        return "User({0} = {1} {2}, {3}, Profile: {4})" \
            .format(self.id, self.first_name, self.last_name, self.email,
                    self.profile.name if self.profile is not None else "?")

    def __repr__(self):
        """User representation."""
        return "User(id={0},firstName='{1}',lastName='{2}',email='{3}',Profile={4})'" \
            .format(self.id, self.first_name, self.last_name, self.email, self.profile)
