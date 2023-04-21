from model.profile_model import Profile

class FeatureStatus:
    """A class to indicate the feature status."""
    NOT_STARTED = "Não Iniciada"
    UNDER_CONSTRUCTION = "Em Construção"
    CONSTRUCTED = "Construída"
    TESTED = "Testada"
    APPROVED = "Aprovada"
    LATE = "Atrasada"
    CANCELED = "Cancelada"

    @classmethod
    def list(cls):
        return [ cls.NOT_STARTED, cls.UNDER_CONSTRUCTION, cls.CONSTRUCTED,
                 cls.TESTED, cls.APPROVED, cls.LATE, cls.CANCELED ]

    @classmethod
    def color(cls, status):
        if status == cls.NOT_STARTED:
            return "#ffffff", "#000000"
        if status == cls.UNDER_CONSTRUCTION:
            return "#ffff00", "#000000"
        if status == cls.LATE:
            return "#ff0000", "#ffffff";
        if status == cls.CONSTRUCTED:
            return "#00ffff", "#000000";
        if status == cls.TESTED:
            return "#00ff00", "#000000";
        if status == cls.APPROVED:
            return "#00aa00", "#000000";
        if status == cls.CANCELED:
            return "#dadada", "#252525";


class ProjectStatus:
    """A class to indicate the project status."""
    INACTIVE = "Inativo"
    ACTIVE = "Ativo"


class UserProfile:
    ADMIN = Profile(1, "Admin")
    GUEST = Profile(2, "Convidado")
    PRODUCT_OWNER = Profile(3, "Product Owner")
    List = [ADMIN, GUEST, PRODUCT_OWNER]
