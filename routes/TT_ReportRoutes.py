from fastapi import APIRouter
from controllers.TT_ReportController import get_time_per_developer, get_task_status_distribution, get_weekly_progress

router = APIRouter()

@router.get("/report/developer-time")
async def time_per_developer():
    return await get_time_per_developer()

@router.get("/report/task-status")
async def task_status_dist():
    return await get_task_status_distribution()

@router.get("/report/weekly-progress")
async def weekly():
    return await get_weekly_progress()
