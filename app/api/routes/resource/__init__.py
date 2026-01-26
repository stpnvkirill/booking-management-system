"""
API endpoints for resource management.

Structure:
- create.py  - POST   /api/resources       - create a resource
- read.py    - GET    /api/resources       - list resources (admin only)
               GET    /api/resources/{id}  - get resource details
- update.py  - PATCH  /api/resources/{id}  - partial update
- delete.py  - DELETE /api/resources/{id}  - delete resource
"""

from fastapi import APIRouter

from .create import router as create_router
from .delete import router as delete_router
from .read import router as read_router
from .update import router as update_router

router = APIRouter(prefix="/resources", tags=["Resource"])

# Include all routers
router.include_router(create_router)
router.include_router(read_router)
router.include_router(update_router)
router.include_router(delete_router)
