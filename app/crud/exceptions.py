from typing import Any, Optional


class CRUDOperationError(Exception):
    """Base exception for CRUD operations."""

    def __init__(self, message: str = "An error occurred during the CRUD operation"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(CRUDOperationError):
    """Raised when a resource or group of resources is not found."""

    def __init__(self, resource_type: str, resource_id: Optional[Any] = None):
        if resource_id is not None:
            message = f"{resource_type} with id {resource_id} was not found."
        else:
            message = f"No {resource_type} resources were found."
        super().__init__(message)


class AuthorizationError(CRUDOperationError):
    """Raised when a user is not authorized to perform an action."""

    def __init__(self, action: str = "perform this action"):
        super().__init__(f"User is not authorized to {action}.")


class DatabaseCommitError(CRUDOperationError):
    """Raised when a database commit fails."""

    def __init__(self, original_exception: Exception):
        self.original_exception = original_exception
        super().__init__("An error occurred while committing changes to the database.")
