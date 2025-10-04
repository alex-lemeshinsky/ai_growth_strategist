"""
API routes for viewing HTML reports directly in browser.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
import logging
import re

from src.db import MongoDB, TaskStatus, PolicyCheckStatus
from src.utils.error_pages import (
    not_found_page,
    still_processing_page,
    task_failed_page,
    no_html_report_page
)

logger = logging.getLogger(__name__)

router = APIRouter()


def validate_uuid(task_id: str) -> bool:
    """Validate UUID format."""
    uuid_pattern = re.compile(
        r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(task_id))


@router.get("/task/{task_id}", response_class=HTMLResponse, summary="View competitor analysis HTML report")
async def view_task_report(task_id: str):
    """
    View HTML report for competitor analysis task.

    Returns:
        - 200: HTML report (if task completed and report generated)
        - 202: Still processing page (if task is pending/analyzing)
        - 404: Not found page (if task doesn't exist)
        - 500: Failed page (if task failed)
    """
    try:
        # Validate UUID format
        if not validate_uuid(task_id):
            logger.warning(f"Invalid task_id format: {task_id}")
            return HTMLResponse(
                content=not_found_page(task_id, "task"),
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Get task from DB
        db = MongoDB.get_db()
        task = await db.tasks.find_one({"task_id": task_id})

        # Task not found
        if not task:
            logger.warning(f"Task not found: {task_id}")
            return HTMLResponse(
                content=not_found_page(task_id, "task"),
                status_code=status.HTTP_404_NOT_FOUND
            )

        task_status = task.get("status")

        # Task failed
        if task_status == TaskStatus.FAILED:
            error = task.get("error", "Unknown error occurred")
            logger.error(f"Task {task_id} failed: {error}")
            return HTMLResponse(
                content=task_failed_page(task_id, error, "task"),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Task still processing
        if task_status in [TaskStatus.PENDING, TaskStatus.PARSING, TaskStatus.PARSED, TaskStatus.ANALYZING]:
            logger.info(f"Task {task_id} still processing: {task_status}")
            return HTMLResponse(
                content=still_processing_page(task_id, task_status, "task"),
                status_code=status.HTTP_202_ACCEPTED
            )

        # Task completed but no HTML report yet
        if task_status == TaskStatus.COMPLETED and not task.get("html_report"):
            logger.warning(f"Task {task_id} completed but no HTML report")
            return HTMLResponse(
                content=no_html_report_page(task_id, "task"),
                status_code=status.HTTP_202_ACCEPTED
            )

        # Return HTML report
        html_report = task.get("html_report")
        if html_report:
            logger.info(f"✅ Serving HTML report for task {task_id}")
            return HTMLResponse(content=html_report, status_code=status.HTTP_200_OK)

        # Fallback: no report available
        logger.error(f"Task {task_id} has no HTML report")
        return HTMLResponse(
            content=no_html_report_page(task_id, "task"),
            status_code=status.HTTP_202_ACCEPTED
        )

    except Exception as e:
        logger.error(f"Error viewing task report {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load report: {str(e)}"
        )


@router.get("/policy/{task_id}", response_class=HTMLResponse, summary="View policy check HTML report")
async def view_policy_report(task_id: str):
    """
    View HTML report for policy check task.

    Returns:
        - 200: HTML report (if task completed and report generated)
        - 202: Still processing page (if task is checking)
        - 404: Not found page (if task doesn't exist)
        - 500: Failed page (if task failed)
    """
    try:
        # Validate UUID format
        if not validate_uuid(task_id):
            logger.warning(f"Invalid task_id format: {task_id}")
            return HTMLResponse(
                content=not_found_page(task_id, "policy"),
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Get task from DB
        db = MongoDB.get_db()
        task = await db.policy_tasks.find_one({"task_id": task_id})

        # Task not found
        if not task:
            logger.warning(f"Policy task not found: {task_id}")
            return HTMLResponse(
                content=not_found_page(task_id, "policy"),
                status_code=status.HTTP_404_NOT_FOUND
            )

        task_status = task.get("status")

        # Task failed
        if task_status == PolicyCheckStatus.FAILED:
            error = task.get("error", "Unknown error occurred")
            logger.error(f"Policy task {task_id} failed: {error}")
            return HTMLResponse(
                content=task_failed_page(task_id, error, "policy"),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Task still processing
        if task_status in [PolicyCheckStatus.PENDING, PolicyCheckStatus.CHECKING]:
            logger.info(f"Policy task {task_id} still processing: {task_status}")
            return HTMLResponse(
                content=still_processing_page(task_id, task_status, "policy"),
                status_code=status.HTTP_202_ACCEPTED
            )

        # Task completed but no HTML report yet
        if task_status == PolicyCheckStatus.COMPLETED and not task.get("html_report"):
            logger.warning(f"Policy task {task_id} completed but no HTML report")
            return HTMLResponse(
                content=no_html_report_page(task_id, "policy"),
                status_code=status.HTTP_202_ACCEPTED
            )

        # Return HTML report
        html_report = task.get("html_report")
        if html_report:
            logger.info(f"✅ Serving HTML report for policy task {task_id}")
            return HTMLResponse(content=html_report, status_code=status.HTTP_200_OK)

        # Fallback: no report available
        logger.error(f"Policy task {task_id} has no HTML report")
        return HTMLResponse(
            content=no_html_report_page(task_id, "policy"),
            status_code=status.HTTP_202_ACCEPTED
        )

    except Exception as e:
        logger.error(f"Error viewing policy report {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load report: {str(e)}"
        )
