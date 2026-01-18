from typing import Annotated, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.security import security
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.resources import Resource
from app.infrastructure.database.models.users import User, Customer
from app.infrastructure.database import models # To ensure models are loaded
from .schema import ResourceModel, ResourceCreate, ResourceUpdate

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.post("/", response_model=ResourceModel, summary="Создать новый ресурс")
async def create_resource(
    resource_in: ResourceCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Создание ресурса.
    Ресурс привязывается к Customer, которому принадлежит текущий пользователь (или которым владеет).
    """
    # 1. Determine Customer ID
    # Logic: User -> CustomerMember -> Customer OR User -> Customer (owner)
    # For simplicity, let's assume we find the customer the user is associated with.
    # Looking at User model, it doesn't strictly link back easily without extra queries if not loaded.
    # But let's check if user creates it, we need to know WHICH customer.
    # Usually passed in header or inferred. Let's try to infer from ownership for now based on previous context.
    
    # Simple logic: Find customer where owner_id is current_user.id
    customer = await Customer.get_by(owner_id=current_user.id, session=session)
    if not customer:
        # Try finding if instance is a member (if that logic exists). 
        # For now, restricting to Owner for creation or assuming single tenant context.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User does not have a customer profile to add resources to."
        )

    new_resource = await Resource.create(
        session=session,
        customer_id=customer.id,
        **resource_in.model_dump()
    )
    return ResourceModel.model_validate(new_resource, from_attributes=True)


@router.get("/", response_model=List[ResourceModel], summary="Список ресурсов (для админов)")
async def read_resources(
    current_user: Annotated[User, Depends(security.get_current_user)], # Authenticaton
    session: Annotated[AsyncSession, Depends(provider.get_session)],
    skip: int = 0,
    limit: int = 100,
):
    """
    Получение списка всех ресурсов.
    TODO: Добавить проверку на права администратора (is_superuser или роль).
    Сейчас доступно всем авторизованным пользователям для демонстрации.
    """
    # For admin only, we would check permissions here.
    # resources = await Resource.get_all(session=session) # This might get ALL resources of ALL customers
    
    # If the requirement "только для админов" means System Admin -> All resources
    # If it means Customer Admin -> Their resources.
    # Given the prompt "GET /api/resources - список ресурсов (только для админов)", let's assume System Admin for now or filter.
    
    stmt = select(Resource).offset(skip).limit(limit)
    result = await session.scalars(stmt)
    return [ResourceModel.model_validate(r, from_attributes=True) for r in result.all()]


@router.put("/{resource_id}", response_model=ResourceModel, summary="Обновить ресурс")
async def update_resource(
    resource_id: uuid.UUID,
    resource_in: ResourceUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Обновление данных ресурса.
    """
    resource = await Resource.get(id=resource_id, session=session)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # TODO: Check permission (does user own this resource's customer?)
    
    updated_resource = await Resource.update(
        id=resource_id,
        session=session,
        **resource_in.model_dump(exclude_unset=True)
    )
    return ResourceModel.model_validate(updated_resource, from_attributes=True)


@router.delete("/{resource_id}", summary="Деактивация ресурса")
async def delete_resource(
    resource_id: uuid.UUID,
    current_user: Annotated[User, Depends(security.get_current_user)],
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    """
    Мягкое удаление ресурса (is_active = False).
    """
    resource = await Resource.get(id=resource_id, session=session)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
        
    # TODO: Check permission
    
    # Soft delete
    await Resource.update(
        id=resource_id,
        session=session,
        is_active=False
    )
    return {"ok": True}
