from fastapi import APIRouter
from typing import Annotated
from fastapi import Path
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

router = APIRouter(prefix="/greet", tags=["Greet"])

executor = ProcessPoolExecutor()

def compute_task(name: str):
    time.sleep(1)
    return f"Hello, {name.title()}!"

@router.get("/{name}")
async def greet(name: Annotated[str, Path()]):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, compute_task, name)
    return result
