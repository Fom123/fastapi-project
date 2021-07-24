from fastapi import APIRouter

from . import not_for_production
from api_v1.endpoints.testpoint import api_router
from .endpoints import oauth
from .endpoints import products
from .endpoints import users


def setup_routers() -> APIRouter:
    api_router.include_router(users.api_router)
    api_router.include_router(oauth.api_router)
    api_router.include_router(products.api_router)
    api_router.include_router(not_for_production.api_router)
    return api_router


__all__ = ("setup_routers",)
