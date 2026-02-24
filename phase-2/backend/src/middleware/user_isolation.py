from fastapi import HTTPException, Request
from functools import wraps
from typing import Callable, Any


def require_user_access(user_id_param: str = "user_id"):
    """
    Middleware decorator to ensure the authenticated user can only access their own resources.

    Args:
        user_id_param: The name of the parameter in the route that contains the user ID to check
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the request object (assuming it's passed as a keyword argument)
            request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, Request)), None)

            if not request:
                raise HTTPException(status_code=400, detail="Request object not found")

            # Get the authenticated user from request state (set by JWT middleware)
            authenticated_user = getattr(request.state, 'user', None)

            if not authenticated_user:
                raise HTTPException(status_code=401, detail="Authentication required")

            # Get the target user ID from path/query parameters
            target_user_id = kwargs.get(user_id_param)

            if not target_user_id:
                # If user_id_param is not in kwargs, try to get it from path_params
                path_params = getattr(request, 'path_params', {})
                target_user_id = path_params.get(user_id_param)

            if not target_user_id:
                # If still not found, try query params
                query_params = getattr(request, 'query_params', {})
                target_user_id = query_params.get(user_id_param)

            # Check if the authenticated user ID matches the target user ID
            if str(authenticated_user.user_id) != str(target_user_id):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied: You can only access your own resources"
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


def check_user_owns_resource(resource_owner_field: str = "user_id"):
    """
    Middleware to check if the authenticated user owns a specific resource.

    Args:
        resource_owner_field: The field name in the resource that contains the owner's user ID
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get the request object
            request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, Request)), None)

            if not request:
                raise HTTPException(status_code=400, detail="Request object not found")

            # Get the authenticated user
            authenticated_user = getattr(request.state, 'user', None)

            if not authenticated_user:
                raise HTTPException(status_code=401, detail="Authentication required")

            # The resource should be passed to the function and checked
            # This is typically done inside the route handler after fetching the resource
            # Here we just prepare the check for use in the route
            kwargs['authenticated_user_id'] = authenticated_user.user_id

            return await func(*args, **kwargs)

        return wrapper
    return decorator