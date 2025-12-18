from fastapi import APIRouter
from typing import Annotated
from fastapi import Path
import time
from celery import Celery
from celery.result import AsyncResult
from celery.states import PENDING, STARTED, SUCCESS, FAILURE, RETRY

router = APIRouter(prefix="/greet", tags=["Greet"])


celery = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def greet_task(self, name):
    if name == "fail":
        raise ValueError("Simulated failure inside Celery task")

    time.sleep(1)
    return f"Hello, {name.title()}!"


@router.get("/{name}")
async def greet(name: Annotated[str, Path()]):
    task = greet_task.delay(name)
    return {"task_id": task.id, "status": "queued"}


@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    result = AsyncResult(task_id, app=celery)

    if result.state == PENDING:
        return {"status": "pending"}

    if result.state == STARTED:
        return {"status": "running"}

    if result.state == RETRY:
        return {"status": "retrying"}

    if result.state == SUCCESS:
        return {"status": "completed", "result": result.result}

    if result.state == FAILURE:
        return {"status": "failed", "error": str(result.result)}

    return {"status": result.state}
