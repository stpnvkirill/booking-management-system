"""PATCH /api/resources/{id} - Partial update of resource data."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.resource import resource_service
from app.infrastructure.database.models.users import User

from .schema import ResourceResponse, ResourceUpdate

router = APIRouter()


@router.patch(
    "/{resource_id}",
    response_model=ResourceResponse,
    summary="Partial update of resource data",
)
async def update_resource(
    resource_id: int,
    resource_in: ResourceUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Update resource data (partial update).

    User must be owner or admin of the customer that owns this resource.
    Only provided fields will be updated.
    """
    update_data = resource_in.model_dump(exclude_unset=True)

    resource = await resource_service.update_resource(
        resource_id=resource_id,
        current_user=current_user,
        session=session,
        **update_data,
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or access denied",
        )

    return resource
