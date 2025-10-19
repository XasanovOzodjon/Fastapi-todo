from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    name: str = Field(max_length=128)
    description: str | None = Field(None)
    category: str | None = Field(None, max_length=64)
    priority: int = Field(default=1, ge=1, le=5)
    

class TaskOut(BaseModel):
    id: int
    name: str
    description: str | None
    status: bool
    user_id: int
    category: str | None
    priority: int

    class Config:
        from_attributes = True
