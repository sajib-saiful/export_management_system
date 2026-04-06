from fastapi import APIRouter

from app.api import auth, buyers, calculations, cost_heads, products, reports, suppliers

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(suppliers.router)
api_router.include_router(buyers.router)
api_router.include_router(cost_heads.router)
api_router.include_router(calculations.router)
api_router.include_router(reports.router)
