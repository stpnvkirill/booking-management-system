"""
GET /api/resources     - List resources for the customer (admin/owner only)
GET /api/resources/{id} - Get resource details
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.resource import resource_service
from app.infrastructure.database.models.users import User

from .schema import ResourceResponse

router = APIRouter()


@router.get(
    "/",
    response_model=list[ResourceResponse],
    summary="List resources for customer",
)
async def list_resources(
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
    customer_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
):
    """Get list of resources for the customer.

    Only returns resources for customers where user is admin or owner.
    If customer_id is not provided, uses the customer where user is owner/admin.
    """
    return await resource_service.get_resources_for_customer(
        current_user=current_user,
        customer_id=customer_id,
        skip=skip,
        limit=limit,
        session=session,
    )


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse,
    summary="Get resource details",
)
async def read_resource(
    resource_id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Get information about a specific resource by ID.

    User must be owner or admin of the customer that owns this resource.
    """
    resource = await resource_service.get_resource(
        resource_id=resource_id,
        current_user=current_user,
        session=session,
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or access denied",
        )

    return resource
