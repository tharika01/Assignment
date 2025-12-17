from typing import Annotated
from fastapi import APIRouter, Path

router = APIRouter(prefix="/greet", tags=["Greet"])


@router.get("/{name}")
async def greet(name: Annotated[str, Path()]):
    return f"Hello, {name.title()}!"
