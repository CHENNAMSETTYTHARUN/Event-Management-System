from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as api_v1_router
from app.core.config import settings
from app.core.database import create_database_if_not_exists, SessionLocal, engine
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.middleware.audit import AuditMiddleware
from app.models.base import Base
from app.models.role import Role
from app.models.user import User
from app.core.security import get_password_hash

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-ready Event Management System Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

register_exception_handlers(app)

app.add_middleware(AuditMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    try:
        create_database_if_not_exists()
    except Exception as e:
        print(f"Error checking/creating database: {e}")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        roles = ["Admin", "Organizer", "Participant"]
        role_map = {}
        for r_name in roles:
            role = db.query(Role).filter(Role.name == r_name).first()
            if not role:
                role = Role(name=r_name)
                db.add(role)
                db.commit()
                db.refresh(role)
            role_map[r_name] = role.id

        admin_email = "admin@example.com"
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            admin_role_id = role_map["Admin"]
            hashed_pass = get_password_hash("admin123")
            admin_user = User(
                full_name="System Admin",
                email=admin_email,
                phone="+1111111111",
                password=hashed_pass,
                role_id=admin_role_id,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Seeded default admin user: admin@example.com / admin123")
    finally:
        db.close()

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENV
    }
