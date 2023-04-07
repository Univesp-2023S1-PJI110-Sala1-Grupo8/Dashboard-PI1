from model.profile_model import Profile

class FeatureStatus:
    """A class to indicate the feature status."""
    NOT_STARTED = "Não Iniciado"
    UNDER_CONSTRUCTION = "Em Construção"
    CONSTRUCTED = "Construída"
    TESTED = "Testada"
    APPROVED = "Aprovada"
    LATE = "Atrasada"
    CANCELED = "Cancelada"


class ProjectStatus:
    """A class to indicate the project status."""
    INACTIVE = "Inativo"
    ACTIVE = "Ativo"


class UserProfile:
    ADMIN = Profile(1, "Admin"),
    GUEST = Profile(2, "Convidado"),
    PRODUCT_OWNER = Profile(3, "Product Owner")
