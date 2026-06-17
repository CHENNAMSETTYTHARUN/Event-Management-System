from pydantic import BaseModel, Field

class RoleBase(BaseModel):
    name: str = Field(..., min_length=2, examples=["Participant"])

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True
