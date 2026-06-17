from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.schemas.ticket import TicketGenerateRequest, TicketResponse, TicketValidateRequest, TicketValidationResponse
from app.services.ticket import ticket_service

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/generate", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def generate_ticket(
    request: TicketGenerateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return ticket_service.generate_ticket(
        db,
        registration_id=request.registration_id,
        user_id=current_user.id,
        is_admin=is_admin,
        background_tasks=background_tasks
    )

@router.get("/{ticket_id}", response_model=TicketResponse)
def view_ticket(
    ticket_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return ticket_service.get_ticket(db, ticket_id=ticket_id, user_id=current_user.id, is_admin=is_admin)

@router.get("/number/{ticket_number}", response_model=TicketResponse)
def view_ticket_by_number(
    ticket_number: str,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return ticket_service.get_ticket_by_number(db, ticket_number=ticket_number, user_id=current_user.id, is_admin=is_admin)

@router.post("/validate", response_model=TicketValidationResponse)
def validate_ticket(
    request: TicketValidateRequest,
    current_user: User = Depends(deps.RoleChecker(allowed_roles=["Organizer"])),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    res = ticket_service.validate_ticket(
        db,
        ticket_number=request.ticket_number,
        event_id=request.event_id,
        user_id=current_user.id,
        is_admin=is_admin
    )
    return res

@router.put("/{ticket_id}/cancel", response_model=TicketResponse)
def cancel_ticket(
    ticket_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role.name == "Admin"
    return ticket_service.cancel_ticket(db, ticket_id=ticket_id, user_id=current_user.id, is_admin=is_admin)
