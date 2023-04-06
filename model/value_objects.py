class FeatureStatus:
    """A class to indicate the feature status."""
    NOT_STARTED = 0  # Não iniciada
    UNDER_CONSTRUCTION = 1  # Em Construção
    CONSTRUCTED = 2  # Contruída
    TESTED = 3  # Testada
    APPROVED = 4  # Aprovada
    LATE = 8  # Atrasada
    CANCELED = 9  # Cancelada

class ProjectStatus:
    """A class to indicate the project status."""
    INACTIVE = 0  # Inativo
    ACTIVE = 1  # Ativo
