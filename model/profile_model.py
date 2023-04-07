from model.base_entity_model import Entity


class Profile(Entity):
    """
    A class to represent the user's profile to access the application.

    Attributes:
        id      The profile unique id.
        name    The profile name.
    """

    def __init__(self, id=0, name=""):
        super().__init__()
        self.id = id
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Profile):
            return False
        return self.__str__() == other.__str__()

    def __str__(self):
        """Profile string."""
        return "Profile({0}='{1}')".format(self.id, self.name)

    def __repr__(self):
        """Profile representation."""
        return "Profile(id={0},name='{1}')'".format(self.id, self.name)
