from fastapi import HTTPException
from datetime import datetime
from collections import defaultdict
from bson import ObjectId
from config.TT_Db import timetracker_user_collection, timetracker_task_collection, timetracker_status_collection

async def get_time_per_developer():
    pipeline = [
        {"$unwind": "$assignedDevelopers"},
        {"$group": {
            "_id": "$assignedDevelopers",
            "totalTime": {"$sum": "$timeSpent"}
        }}
    ]
    data = await timetracker_task_collection.aggregate(pipeline).to_list(length=None)
    result = []

    for d in data:
        user = await timetracker_user_collection.find_one({"_id": ObjectId(d["_id"])})
        if user:
            result.append({
                "username": user["username"],
                "totalTime": d["totalTime"]
            })
    return result

async def get_task_status_distribution():
    pipeline = [
        {"$group": {
            "_id": "$statusId",
            "count": {"$sum": 1}
        }}
    ]
    data = await timetracker_task_collection.aggregate(pipeline).to_list(length=None)
    result = []

    for d in data:
        status = await timetracker_status_collection.find_one({"_id": ObjectId(d["_id"])})
        if status:
            result.append({
                "statusName": status["statusName"],
                "count": d["count"]
            })
    return result

async def get_weekly_progress():
    pipeline = [
        {
            "$project": {
                "timeSpent": 1,
                "dayOfWeek": {"$dayOfWeek": {"$toDate": "$_id"}}
            }
        },
        {
            "$group": {
                "_id": "$dayOfWeek",
                "totalTimeSpent": {"$sum": "$timeSpent"}
            }
        }
    ]

    data = await timetracker_task_collection.aggregate(pipeline).to_list(length=None)
    week_map = {1: "Sun", 2: "Mon", 3: "Tue", 4: "Wed", 5: "Thu", 6: "Fri", 7: "Sat"}
    actual = {week_map.get(d["_id"], "Unknown"): d["totalTimeSpent"] for d in data}

    # Sample static planned values (can be made dynamic)
    planned = {day: 8 for day in week_map.values()}

    return {"planned": planned, "actual": actual}
