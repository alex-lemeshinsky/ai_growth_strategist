#!/usr/bin/env python3
"""
Enhanced script to regenerate HTML reports for tasks with advanced features.
This script extends the basic regeneration with:
- Specific task ID targeting
- Date-based filtering
- Force regeneration option
- Batch processing with progress
- Validation checks
"""
import asyncio
import logging
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
from dotenv import load_dotenv

from src.db import MongoDB, TaskStatus
from src.utils.html_report import generate_html_report

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_completed_tasks_with_filters(
    limit: Optional[int] = None,
    since_date: Optional[datetime] = None,
    task_ids: Optional[List[str]] = None,
    include_without_html: bool = False,
    only_without_html: bool = False
) -> List[Dict[str, Any]]:
    """Get completed tasks with advanced filtering options."""
    db = MongoDB.get_db()
    
    # Build query
    query = {"status": TaskStatus.COMPLETED}
    
    # Date filter
    if since_date:
        query["updated_at"] = {"$gte": since_date}
    
    # Specific task IDs
    if task_ids:
        query["task_id"] = {"$in": task_ids}
    
    # HTML report filter
    if only_without_html:
        query["html_report"] = {"$exists": False}
    elif not include_without_html:
        query["html_report"] = {"$exists": True}
    
    # Build cursor
    cursor = db.tasks.find(query).sort("updated_at", -1)
    
    if limit:
        cursor = cursor.limit(limit)
    
    tasks = await cursor.to_list(length=limit or 1000)
    
    # Remove MongoDB _id field
    for task in tasks:
        task.pop("_id", None)
    
    return tasks


async def validate_task_data(task: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and enhance task data before regeneration."""
    task_id = task.get("task_id")
    validation_result = {
        "task_id": task_id,
        "valid": True,
        "issues": [],
        "warnings": []
    }
    
    # Check required fields
    if not task.get("creatives_analyzed"):
        validation_result["valid"] = False
        validation_result["issues"].append("No analyzed creatives found")
    
    if not task.get("page_name"):
        validation_result["warnings"].append("Missing page_name")
    
    # Check aggregated analysis
    if not task.get("aggregated_analysis") and not task.get("aggregation_error"):
        validation_result["warnings"].append("Missing aggregated analysis")
    
    # Check video URLs and cached paths
    creatives = task.get("creatives_analyzed", [])
    videos_with_issues = 0
    for creative in creatives:
        if not creative.get("video_url") and not creative.get("cached_video_path"):
            videos_with_issues += 1
    
    if videos_with_issues > 0:
        validation_result["warnings"].append(f"{videos_with_issues} creatives missing video URLs")
    
    return validation_result


async def regenerate_task_html_report_enhanced(
    task: Dict[str, Any], 
    force: bool = False,
    validate: bool = True
) -> Dict[str, Any]:
    """Enhanced HTML report regeneration with validation and detailed results."""
    task_id = task.get("task_id")
    result = {
        "task_id": task_id,
        "success": False,
        "validation": None,
        "error": None,
        "time_taken": 0
    }
    
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"🔄 Processing task: {task_id}")
        
        # Validation
        if validate:
            validation = await validate_task_data(task)
            result["validation"] = validation
            
            if not validation["valid"] and not force:
                result["error"] = f"Validation failed: {', '.join(validation['issues'])}"
                return result
            
            if validation["warnings"]:
                logger.warning(f"⚠️ Task {task_id} has warnings: {', '.join(validation['warnings'])}")
        
        # Check if regeneration is needed
        existing_html = task.get("html_report")
        if existing_html and not force:
            logger.info(f"⏭️ Task {task_id} already has HTML report, skipping (use --force to override)")
            result["success"] = True
            result["error"] = "Skipped - already has HTML"
            return result
        
        # Prepare enhanced task data
        task_data = {
            "task_id": task_id,
            "page_name": task.get("page_name", "Unknown"),
            "total_ads": task.get("total_ads", 0),
            "source_url": task.get("url", ""),  # Original URL
        }
        
        # Get creatives data
        creatives_analyzed = task.get("creatives_analyzed", [])
        if not creatives_analyzed:
            result["error"] = "No analyzed creatives found"
            return result
        
        # Get aggregated analysis
        aggregated_analysis = task.get("aggregated_analysis")
        aggregation_error = task.get("aggregation_error")
        
        # Generate new HTML report
        logger.debug(f"🎨 Generating HTML for task {task_id}")
        html_report = generate_html_report(
            task_data=task_data,
            creatives=creatives_analyzed,
            aggregated=aggregated_analysis,
            aggregation_error=aggregation_error
        )
        
        if not html_report:
            result["error"] = "HTML generation returned empty result"
            return result
        
        # Update task in database
        logger.debug(f"💾 Updating database for task {task_id}")
        db = MongoDB.get_db()
        update_result = await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {
                "html_report": html_report,
                "updated_at": datetime.utcnow(),
                "html_regenerated_at": datetime.utcnow()
            }}
        )
        
        if update_result.modified_count > 0:
            result["success"] = True
            logger.info(f"✅ Successfully updated HTML report for task {task_id}")
        else:
            result["error"] = "Database update failed"
            
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"❌ Error processing task {task_id}: {e}")
    
    finally:
        end_time = datetime.utcnow()
        result["time_taken"] = (end_time - start_time).total_seconds()
    
    return result


async def regenerate_reports_enhanced(
    limit: Optional[int] = None,
    since_date: Optional[datetime] = None,
    task_ids: Optional[List[str]] = None,
    force: bool = False,
    validate: bool = True,
    batch_size: int = 5
):
    """Enhanced regeneration with batch processing and detailed reporting."""
    logger.info("🚀 Starting enhanced HTML report regeneration")
    
    # Get tasks based on filters
    logger.info("📋 Fetching tasks...")
    tasks = await get_completed_tasks_with_filters(
        limit=limit,
        since_date=since_date,
        task_ids=task_ids,
        include_without_html=True
    )
    
    if not tasks:
        logger.info("🤷 No tasks found matching criteria")
        return
    
    logger.info(f"📋 Found {len(tasks)} tasks to process:")
    for i, task in enumerate(tasks[:10], 1):  # Show first 10
        task_id = task.get("task_id")
        page_name = task.get("page_name", "Unknown")
        creatives_count = len(task.get("creatives_analyzed", []))
        has_html = "✓" if task.get("html_report") else "✗"
        logger.info(f"  {i}. {task_id} - {page_name} ({creatives_count} creatives) [HTML: {has_html}]")
    
    if len(tasks) > 10:
        logger.info(f"  ... and {len(tasks) - 10} more tasks")
    
    # Process in batches
    results = {
        "total": len(tasks),
        "successful": 0,
        "failed": 0,
        "skipped": 0,
        "errors": []
    }
    
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        logger.info(f"🔄 Processing batch {i//batch_size + 1}/{(len(tasks)-1)//batch_size + 1} ({len(batch)} tasks)")
        
        # Process batch
        batch_results = await asyncio.gather(
            *[regenerate_task_html_report_enhanced(task, force=force, validate=validate) 
              for task in batch],
            return_exceptions=True
        )
        
        # Collect results
        for result in batch_results:
            if isinstance(result, Exception):
                results["failed"] += 1
                results["errors"].append(f"Exception: {str(result)}")
                continue
                
            if result["success"]:
                if "Skipped" in result.get("error", ""):
                    results["skipped"] += 1
                else:
                    results["successful"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(f"{result['task_id']}: {result.get('error', 'Unknown error')}")
        
        # Progress update
        processed = min(i + batch_size, len(tasks))
        logger.info(f"📊 Progress: {processed}/{len(tasks)} tasks processed")
    
    # Final summary
    logger.info("🏁 HTML report regeneration completed!")
    logger.info(f"📊 Results:")
    logger.info(f"   ✅ Successfully regenerated: {results['successful']}")
    logger.info(f"   ⏭️ Skipped (already had HTML): {results['skipped']}")
    logger.info(f"   ❌ Failed: {results['failed']}")
    
    if results["errors"]:
        logger.error("❌ Errors encountered:")
        for error in results["errors"][:5]:  # Show first 5 errors
            logger.error(f"   • {error}")
        if len(results["errors"]) > 5:
            logger.error(f"   ... and {len(results['errors']) - 5} more errors")
    
    if results["successful"] > 0:
        logger.info("🎉 Enhanced features in regenerated reports:")
        logger.info("   - Updated video streaming with source URLs")
        logger.info("   - Improved chat integration with task IDs")
        logger.info("   - Enhanced visual design and responsive layout")
        logger.info("   - Better error handling and fallback options")


async def main():
    """Enhanced entry point with more command line options."""
    parser = argparse.ArgumentParser(description="Enhanced HTML report regeneration")
    
    # Basic options
    parser.add_argument(
        "--limit", "-n",
        type=int,
        help="Number of tasks to regenerate (default: all matching)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List tasks that would be regenerated without actually doing it"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration even if HTML already exists"
    )
    
    # Filtering options
    parser.add_argument(
        "--task-ids",
        nargs="+",
        help="Specific task IDs to regenerate (space-separated)"
    )
    parser.add_argument(
        "--since-days",
        type=int,
        help="Only regenerate tasks updated within last N days"
    )
    parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Only regenerate tasks that don't have HTML reports"
    )
    
    # Processing options
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of tasks to process simultaneously (default: 5)"
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip validation checks"
    )
    
    args = parser.parse_args()
    
    # Initialize MongoDB
    try:
        await MongoDB.connect()
        logger.info("✅ MongoDB connected successfully")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        return
    
    try:
        # Calculate since_date if specified
        since_date = None
        if args.since_days:
            since_date = datetime.utcnow() - timedelta(days=args.since_days)
            logger.info(f"📅 Filtering tasks since: {since_date.strftime('%Y-%m-%d %H:%M')}")
        
        # Dry run mode
        if args.dry_run:
            logger.info("🔍 DRY RUN: Listing tasks that would be processed")
            tasks = await get_completed_tasks_with_filters(
                limit=args.limit,
                since_date=since_date,
                task_ids=args.task_ids,
                only_without_html=args.only_missing
            )
            
            if not tasks:
                logger.info("🤷 No tasks found matching criteria")
                return
            
            logger.info(f"📋 Would process {len(tasks)} tasks:")
            for i, task in enumerate(tasks, 1):
                task_id = task.get("task_id")
                page_name = task.get("page_name", "Unknown")
                creatives_count = len(task.get("creatives_analyzed", []))
                updated_at = task.get("updated_at", "Unknown")
                has_html = "✓" if task.get("html_report") else "✗"
                logger.info(f"  {i}. {task_id} - {page_name} ({creatives_count} creatives) - {updated_at} [HTML: {has_html}]")
            
            logger.info("🔄 To actually regenerate, run without --dry-run flag")
        else:
            # Actual regeneration
            await regenerate_reports_enhanced(
                limit=args.limit,
                since_date=since_date,
                task_ids=args.task_ids,
                force=args.force,
                validate=not args.no_validate,
                batch_size=args.batch_size
            )
        
    finally:
        # Close MongoDB connection
        try:
            await MongoDB.close()
            logger.info("✅ MongoDB disconnected successfully")
        except Exception as e:
            logger.error(f"❌ Error disconnecting MongoDB: {e}")


if __name__ == "__main__":
    asyncio.run(main())