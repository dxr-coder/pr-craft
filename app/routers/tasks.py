from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.database import models
from app.database.depends import get_db

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


@router.get("/")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.id.asc()).all()
    return tasks


@router.post("/")
def create_task(
    issue: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    task = models.Task(issue=issue, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)

    background_tasks.add_task(run_workflow, task.id, issue)

    return {"id": task.id, "status": task.status, "message": "任务已创建，后台运行中"}


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "任务不存在"}
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return {"error": "任务不存在"}
    db.delete(task)
    db.commit()
    return {"message": "任务已删除"}


def run_workflow(task_id: int, issue: str):
    import time

    from app.agents.orchestrator import build_graph
    from app.database.connection import SessionLocal
    from app.github.pr_manager import create_branch, create_file, create_pr

    db = SessionLocal()
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return

    try:
        task.status = "processing"
        db.commit()

        graph = build_graph()
        result = graph.invoke(
            {
                "issue": issue,
                "plan": "",
                "code": "",
                "review": "",
                "attempts": 0,
            }
        )

        task.plan = result["plan"]
        task.code = result["code"]
        task.review = result["review"]

        if "PASS" in result["review"]:
            branch = f"auto-pr-{int(time.time())}"
            create_branch(branch)
            create_file(
                branch_name=branch,
                file_path="app/generated/feature.py",
                content=result["code"],
                message=f"AI 自动生成：{issue[:30]}",
            )
            url = create_pr(
                title=f"AI 自动生成：{issue[:50]}",
                body=f"## 需求\n{issue}\n\n## 审查\n{result['review']}",
                branch_name=branch,
            )
            task.branch = branch
            task.pr_url = url
            task.status = "done"
        else:
            task.status = "failed"

    except Exception as e:
        task.status = "failed"
        logger.error(f"工作流出错 task_id={task_id}: {e}")
    finally:
        db.commit()
        db.close()
