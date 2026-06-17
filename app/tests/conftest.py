import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def db_tables():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    from app.models.role import Role
    roles = ["Admin", "Organizer", "Participant"]
    for r_name in roles:
        if not db.query(Role).filter(Role.name == r_name).first():
            db.add(Role(name=r_name))
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_headers(client, db_session):
    from app.models.user import User
    admin = db_session.query(User).filter(User.email == "testadmin@example.com").first()
    if not admin:
        admin = User(
            full_name="Test Admin",
            email="testadmin@example.com",
            phone="+9999999999",
            password=get_password_hash("password123"),
            role_id=1,
            is_active=True
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "testadmin@example.com", "password": "password123"}
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

@pytest.fixture(scope="function")
def organizer_headers(client, db_session):
    from app.models.user import User
    organizer = db_session.query(User).filter(User.email == "testorganizer@example.com").first()
    if not organizer:
        organizer = User(
            full_name="Test Organizer",
            email="testorganizer@example.com",
            phone="+8888888888",
            password=get_password_hash("password123"),
            role_id=2,
            is_active=True
        )
        db_session.add(organizer)
        db_session.commit()
        db_session.refresh(organizer)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "testorganizer@example.com", "password": "password123"}
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

@pytest.fixture(scope="function")
def participant_headers(client, db_session):
    from app.models.user import User
    participant = db_session.query(User).filter(User.email == "testparticipant@example.com").first()
    if not participant:
        participant = User(
            full_name="Test Participant",
            email="testparticipant@example.com",
            phone="+7777777777",
            password=get_password_hash("password123"),
            role_id=3,
            is_active=True
        )
        db_session.add(participant)
        db_session.commit()
        db_session.refresh(participant)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "testparticipant@example.com", "password": "password123"}
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}
