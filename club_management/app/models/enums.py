import enum

class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class MemberRole(str, enum.Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"

class ActivityStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class ActivityPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"