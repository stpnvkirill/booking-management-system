"""Resource service for handling resource business logic with multitenancy support."""

from dataclasses import dataclass
from uuid import UUID

import sqlalchemy as sa

from app.depends import AsyncSession, provider
from app.infrastructure.database.models.booking import Resource
from app.infrastructure.database.models.users import Customer, CustomerAdmin, User


@dataclass(frozen=True)
class ResourceCreateParams:
    name: str
    customer_id: UUID | None = None
    description: str | None = None
    resource_type: str | None = None
    location: str | None = None
    price_per_hour: int | None = None


@dataclass(frozen=True)
class ResourceUpdateParams:
    name: str | None = None
    description: str | None = None
    resource_type: str | None = None
    location: str | None = None
    price_per_hour: int | None = None


class ResourceService:
    """Service for resource CRUD operations with multitenancy checks."""

    @provider.inject_session
    async def is_admin_or_owner(
        self,
        user_id: UUID,
        customer_id: UUID,
        session: AsyncSession | None = None,
    ) -> bool:
        """Check if user is admin or owner of the customer."""
        # Check if owner
        customer = await Customer.get_by(
            id=customer_id,
            owner_id=user_id,
            session=session,
        )
        if customer:
            return True

        # Check if admin
        admin = await CustomerAdmin.get_by(
            user_id=user_id,
            customer_id=customer_id,
            session=session,
        )
        return admin is not None

    @provider.inject_session
    async def get_customer_for_user(
        self,
        user_id: UUID,
        session: AsyncSession | None = None,
    ) -> Customer | None:
        """Get customer where user is owner or admin."""
        # First check if user is owner
        customer = await Customer.get_by(owner_id=user_id, session=session)
        if customer:
            return customer

        # Check if user is admin of any customer
        admin_record = await CustomerAdmin.get_by(user_id=user_id, session=session)
        if admin_record:
            return await Customer.get(id=admin_record.customer_id, session=session)

        return None

    @provider.inject_session
    async def create_resource(
        self,
        current_user: User,
        params: ResourceCreateParams,
        session: AsyncSession | None = None,
    ) -> Resource | None:
        """Create a new resource for a customer.

        If customer_id is not provided, uses the customer where user is owner/admin.
        """
        # Determine customer_id
        customer_id = params.customer_id
        if customer_id is None:
            customer = await self.get_customer_for_user(
                user_id=current_user.id,
                session=session,
            )
            if not customer:
                return None
            customer_id = customer.id
        # Verify user has permission for this customer
        elif not await self.is_admin_or_owner(
            user_id=current_user.id,
            customer_id=customer_id,
            session=session,
        ):
            return None

        resource = Resource(
            customer_id=customer_id,
            name=params.name,
            description=params.description,
            resource_type=params.resource_type,
            location=params.location,
            price_per_hour=params.price_per_hour,
        )
        session.add(resource)
        await session.flush()
        await session.refresh(resource)
        return resource

    @provider.inject_session
    async def get_resources_for_customer(
        self,
        current_user: User,
        customer_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession | None = None,
    ) -> list[Resource]:
        """Get resources filtered by customer (multitenancy).

        Only returns resources for customers where user is admin or owner.
        """
        if customer_id is None:
            customer = await self.get_customer_for_user(
                user_id=current_user.id,
                session=session,
            )
            if not customer:
                return []
            customer_id = customer.id
        elif not await self.is_admin_or_owner(
            user_id=current_user.id,
            customer_id=customer_id,
            session=session,
        ):
            return []

        stmt = (
            sa.select(Resource)
            .where(Resource.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.scalars(stmt)
        return list(result.all())

    @provider.inject_session
    async def get_resource(
        self,
        resource_id: int,
        current_user: User,
        session: AsyncSession | None = None,
    ) -> Resource | None:
        """Get a single resource with permission check."""
        stmt = sa.select(Resource).where(Resource.id == resource_id)
        resource = await session.scalar(stmt)

        if not resource:
            return None

        # Check permission
        if not await self.is_admin_or_owner(
            user_id=current_user.id,
            customer_id=resource.customer_id,
            session=session,
        ):
            return None

        return resource

    @provider.inject_session
    async def update_resource(
        self,
        resource_id: int,
        current_user: User,
        params: ResourceUpdateParams,
        session: AsyncSession | None = None,
    ) -> Resource | None:
        """Update resource with permission check."""
        resource = await self.get_resource(
            resource_id=resource_id,
            current_user=current_user,
            session=session,
        )
        if not resource:
            return None

        if params.name is not None:
            resource.name = params.name
        if params.description is not None:
            resource.description = params.description
        if params.resource_type is not None:
            resource.resource_type = params.resource_type
        if params.location is not None:
            resource.location = params.location
        if params.price_per_hour is not None:
            resource.price_per_hour = params.price_per_hour

        await session.flush()
        await session.refresh(resource)
        return resource

    @provider.inject_session
    async def get_all_resources(
        self,
        skip: int = 0,
        limit: int = 100,
        session: AsyncSession | None = None,
    ) -> list[Resource]:
        """Get all resources (no multitenancy filter)."""
        stmt = sa.select(Resource).offset(skip).limit(limit)
        result = await session.scalars(stmt)
        return list(result.all())

    @provider.inject_session
    async def delete_resource(
        self,
        resource_id: int,
        current_user: User,
        session: AsyncSession | None = None,
    ) -> bool:
        """Delete resource with permission check.

        Note: Currently performs hard delete as model lacks is_active field.
        """
        resource = await self.get_resource(
            resource_id=resource_id,
            current_user=current_user,
            session=session,
        )
        if not resource:
            return False

        await session.delete(resource)
        return True


resource_service = ResourceService()
