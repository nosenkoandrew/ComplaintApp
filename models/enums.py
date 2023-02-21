import enum


class RoleType(enum.Enum):
    approver = "approver"
    admin = "admin"
    complainer = "complainer"


class State(enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
