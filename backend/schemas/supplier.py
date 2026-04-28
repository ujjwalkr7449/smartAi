from pydantic import BaseModel, EmailStr


class SupplierCreateRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str


class SupplierUpdateRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class SupplierResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    address: str

    model_config = {"from_attributes": True}
