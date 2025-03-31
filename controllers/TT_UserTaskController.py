from models.TT_UserTask import UserTask,UserTaskOut
from bson import ObjectId
from config.TT_Db import timetracker_user_task_collection,timetracker_user_collection,timetracker_task_collection, timetracker_status_collection
from fastapi.responses import JSONResponse

async def addUserTask(user_task:UserTask):
    savedUserTask=await timetracker_user_task_collection.insert_one(user_task.dict())
    return JSONResponse(content={"message":"User Task added successfully"})

async def getUserTask():
    userTasks = await timetracker_user_task_collection.find().to_list(length=None)
    print(userTasks)
    for user_task in userTasks:

        # Fetch user details
        if "userId" in user_task:
            user_data = await timetracker_user_collection.find_one({"_id": ObjectId(user_task["userId"])})
            if user_data:
                user_data["_id"] = str(user_data["_id"])
                user_task["user_id"] = user_data
                if "statusId" in user_data:
                    status_data = await timetracker_status_collection.find_one({"_id": ObjectId(user_data["statusId"])})
                    if status_data:
                        status_data["_id"] = str(status_data["_id"])
                        user_data["status_id"] = status_data
                    else:
                        user_data["status_id"] = None
            else:
                user_task["user_id"] = None

        # Fetch task details
        if "taskId" in user_task:
            task_data = await timetracker_task_collection.find_one({"_id": ObjectId(user_task["taskId"])})
            if task_data:
                task_data["_id"] = str(task_data["_id"])
                user_task["task_id"] = task_data
            else:
                user_task["task_id"] = None

    return [UserTaskOut(**user_task) for user_task in userTasks]