"""POST /api/resources - Create a new resource."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security import security
from app.depends import AsyncSession, provider
from app.domain.services.resource import resource_service
from app.infrastructure.database.models.users import User

from .schema import ResourceCreate, ResourceResponse

router = APIRouter()


@router.post(
    "/",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new resource",
)
async def create_resource(
    data: ResourceCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """Create a new resource.

    User must be owner or admin of the customer to create resources.
    If customer_id is not provided, uses the customer where user is owner/admin.
    """
    resource = await resource_service.create_resource(
        current_user=current_user,
        name=data.name,
        customer_id=data.customer_id,
        session=session,
    )

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No permission to create resources for this customer",
        )

    return resource
