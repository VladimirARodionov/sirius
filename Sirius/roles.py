from rolepermissions.roles import AbstractUserRole


class AdminRole(AbstractUserRole):
    available_permissions = {}


class UserRole(AbstractUserRole):
    available_permissions = {
    }


class ReportsRole(AbstractUserRole):
    available_permissions = {
    }


class ActionsRole(AbstractUserRole):
    available_permissions = {
    }


class UserListRole(AbstractUserRole):
    available_permissions = {
    }


class UserDetailRole(AbstractUserRole):
    available_permissions = {
    }

