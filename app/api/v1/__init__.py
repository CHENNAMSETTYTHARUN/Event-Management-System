from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.roles import router as roles_router
from app.api.v1.categories import router as categories_router
from app.api.v1.events import router as events_router
from app.api.v1.registrations import router as registrations_router
from app.api.v1.tickets import router as tickets_router
from app.api.v1.attendance import router as attendance_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.reports import router as reports_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(roles_router)
router.include_router(categories_router)
router.include_router(events_router)
router.include_router(registrations_router)
router.include_router(tickets_router)
router.include_router(attendance_router)
router.include_router(dashboard_router)
router.include_router(reports_router)
