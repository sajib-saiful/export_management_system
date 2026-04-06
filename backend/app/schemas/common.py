from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    company_name: str
    full_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    company_id: int
    full_name: str
    email: EmailStr
    role_id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    category: str | None = None
    grade: str | None = None
    unit: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True


class ProductPriceCreate(BaseModel):
    product_id: int
    date: date
    price: float


class ProductPriceOut(BaseModel):
    id: int
    product_id: int
    date: date
    price: float

    class Config:
        from_attributes = True


class SupplierBase(BaseModel):
    name: str
    phone: str | None = None
    district: str | None = None
    address: str | None = None


class SupplierCreate(SupplierBase):
    pass


class SupplierOut(SupplierBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True


class BuyerBase(BaseModel):
    name: str
    company_name: str | None = None
    country: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


class BuyerCreate(BuyerBase):
    pass


class BuyerOut(BuyerBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True


class CostHeadBase(BaseModel):
    name: str
    type: str
    is_active: bool = True


class CostHeadCreate(CostHeadBase):
    pass


class CostHeadOut(CostHeadBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True


class CostEntryInput(BaseModel):
    cost_head_id: int
    amount: float


class CalculationCreate(BaseModel):
    product_id: int
    entries: list[CostEntryInput]


class CalculationOut(BaseModel):
    id: int
    company_id: int
    product_id: int
    total_fob: float
    total_cfr: float
    total_cpt: float
    created_at: datetime

    class Config:
        from_attributes = True
