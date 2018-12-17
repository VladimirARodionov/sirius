from rolepermissions.roles import AbstractUserRole


class AdminRole(AbstractUserRole):
    available_permissions = {}


class UserRole(AbstractUserRole):
    available_permissions = {
    }
