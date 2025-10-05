#!/usr/bin/env python3
"""
Script to regenerate HTML reports for the last N tasks with improved formatting.
This script will update existing completed tasks with new HTML reports that include
better strategy display and chat buttons.
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

from src.db import MongoDB, TaskStatus
from src.utils.html_report import generate_html_report

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_last_completed_tasks(limit: int = 10) -> List[Dict[str, Any]]:
    """Get the last N completed tasks from the database."""
    db = MongoDB.get_db()
    
    cursor = db.tasks.find(
        {"status": TaskStatus.COMPLETED}
    ).sort("updated_at", -1).limit(limit)
    
    tasks = await cursor.to_list(length=limit)
    
    # Remove MongoDB _id field for easier processing
    for task in tasks:
        task.pop("_id", None)
    
    return tasks


async def regenerate_task_html_report(task: Dict[str, Any]) -> bool:
    """Regenerate HTML report for a single task."""
    task_id = task.get("task_id")
    logger.info(f"🔄 Regenerating HTML report for task: {task_id}")
    
    try:
        # Prepare task data
        task_data = {
            "task_id": task_id,  # Include task_id for chat button
            "page_name": task.get("page_name", "Unknown"),
            "total_ads": task.get("total_ads", 0),
        }
        
        # Get creatives data
        creatives_analyzed = task.get("creatives_analyzed", [])
        if not creatives_analyzed:
            logger.warning(f"⚠️ Task {task_id} has no analyzed creatives")
            return False
        
        # Get aggregated analysis
        aggregated_analysis = task.get("aggregated_analysis")
        aggregation_error = task.get("aggregation_error")
        
        # Generate new HTML report with improvements
        html_report = generate_html_report(
            task_data=task_data,
            creatives=creatives_analyzed,
            aggregated=aggregated_analysis,
            aggregation_error=aggregation_error
        )
        
        if not html_report:
            logger.error(f"❌ Failed to generate HTML report for task {task_id}")
            return False
        
        # Update task in database with new HTML report
        db = MongoDB.get_db()
        result = await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "html_report": html_report,
                "updated_at": datetime.utcnow()
            }}
        )
        
        if result.modified_count > 0:
            logger.info(f"✅ Successfully updated HTML report for task {task_id}")
            return True
        else:
            logger.warning(f"⚠️ No documents updated for task {task_id}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error regenerating HTML report for task {task_id}: {e}")
        return False


async def regenerate_reports(limit: int = 10):
    """Main function to regenerate HTML reports for last N tasks."""
    logger.info(f"🚀 Starting HTML report regeneration for last {limit} completed tasks")
    
    # Get completed tasks
    tasks = await get_last_completed_tasks(limit)
    
    if not tasks:
        logger.info("🤷 No completed tasks found")
        return
    
    logger.info(f"📋 Found {len(tasks)} completed tasks to regenerate:")
    for i, task in enumerate(tasks, 1):
        task_id = task.get("task_id")
        page_name = task.get("page_name", "Unknown")
        creatives_count = len(task.get("creatives_analyzed", []))
        updated_at = task.get("updated_at", "Unknown")
        logger.info(f"  {i}. {task_id} - {page_name} ({creatives_count} creatives) - {updated_at}")
    
    # Regenerate reports
    successful = 0
    failed = 0
    
    for task in tasks:
        success = await regenerate_task_html_report(task)
        if success:
            successful += 1
        else:
            failed += 1
    
    logger.info(f"🏁 HTML report regeneration completed!")
    logger.info(f"✅ Successfully regenerated: {successful}")
    logger.info(f"❌ Failed to regenerate: {failed}")
    
    if successful > 0:
        logger.info(f"🎉 {successful} tasks now have improved HTML reports with:")
        logger.info("   - Better strategy display with icons and colors")
        logger.info("   - Chat buttons for creating new sessions")
        logger.info("   - Enhanced visual design")


async def main():
    """Entry point for the script."""
    import argparse
    
    # Initialize MongoDB connection
    try:
        await MongoDB.connect()
        logger.info("✅ MongoDB connected successfully")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        return
    
    try:
        parser = argparse.ArgumentParser(description="Regenerate HTML reports with improvements")
        parser.add_argument(
            "--limit", "-n",
            type=int,
            default=10,
            help="Number of last completed tasks to regenerate (default: 10)"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List tasks that would be regenerated without actually doing it"
        )
        
        args = parser.parse_args()
        
        if args.dry_run:
            logger.info(f"🔍 DRY RUN: Listing last {args.limit} completed tasks that would be regenerated")
            tasks = await get_last_completed_tasks(args.limit)
            
            if not tasks:
                logger.info("🤷 No completed tasks found")
                return
            
            logger.info(f"📋 Would regenerate HTML reports for {len(tasks)} tasks:")
            for i, task in enumerate(tasks, 1):
                task_id = task.get("task_id")
                page_name = task.get("page_name", "Unknown")
                creatives_count = len(task.get("creatives_analyzed", []))
                updated_at = task.get("updated_at", "Unknown")
                has_html = bool(task.get("html_report"))
                logger.info(f"  {i}. {task_id} - {page_name} ({creatives_count} creatives) - {updated_at} [HTML: {'✓' if has_html else '✗'}]")
            
            logger.info("🔄 To actually regenerate, run without --dry-run flag")
        else:
            await regenerate_reports(args.limit)
        
    finally:
        # Close MongoDB connection
        try:
            await MongoDB.close()
            logger.info("✅ MongoDB disconnected successfully")
        except Exception as e:
            logger.error(f"❌ Error disconnecting MongoDB: {e}")


if __name__ == "__main__":
    asyncio.run(main())