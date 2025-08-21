from pydantic import BaseModel, Field


class DepartmentOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DepartmentPatch(BaseModel):
    name: str | None = Field(None, max_length=255)
