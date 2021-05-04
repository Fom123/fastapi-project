from typing import Optional

import fastapi.responses
from dependency_injector.wiring import inject, Provide
from fastapi import Header, Body, Depends

from api.application import api_router
from services.db.crud import ProductRepository
from services.dependencies.containers import Application
from services.misc import DefaultResponse
from services.misc.schemas import Product, User
from services.utils.responses import bad_response
from services.utils.security import get_current_user


@api_router.put("/products/create", tags=["Product"],
                responses={400: {"model": DefaultResponse}}, status_code=201)
@inject
async def create_product(
        product: Product = Body(..., example={
            "name": "Apple MacBook 15",
            "unit_price": 7000,
            "description": "Light and fast laptop",
            "size": "S"
        }),
        user_agent: Optional[str] = Header(None, title="User-Agent"),
        product_crud: ProductRepository = Depends(
            Provide[Application.services.user_repository]
        ),
        user: User = Depends(get_current_user)
):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **unit_price**: required
    - **size**: size of item
    """
    if not user_agent:
        return bad_response()
    await product_crud.add(**product.dict(exclude_unset=True))
    return fastapi.responses.Response(status_code=201,
                                      headers={
                                          "User-Agent": user_agent
                                      })
