#!/usr/bin/env python3
"""
Test script for HTML report viewer endpoints.

Usage:
    python test_report_viewer.py
"""
import asyncio
from src.db import MongoDB, Task, PolicyTask, TaskStatus, PolicyCheckStatus
import uuid


async def test_report_viewer():
    """Test report viewer endpoints with different scenarios."""

    print("🧪 Testing HTML Report Viewer Endpoints\n")

    # Connect to MongoDB
    await MongoDB.connect()
    db = MongoDB.get_db()

    # Test scenarios
    test_cases = []

    # 1. Create a PENDING task
    pending_id = str(uuid.uuid4())
    pending_task = Task(
        task_id=pending_id,
        url="https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id=123456",
        status=TaskStatus.PENDING
    )
    await db.tasks.insert_one(pending_task.model_dump())
    test_cases.append(("PENDING Task", pending_id, "/report/task/"))

    # 2. Create a COMPLETED task with HTML report
    completed_id = str(uuid.uuid4())
    completed_task = Task(
        task_id=completed_id,
        url="https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id=789012",
        status=TaskStatus.COMPLETED,
        page_name="Test Page",
        total_ads=5,
        html_report="<html><body><h1>Test Report</h1></body></html>"
    )
    await db.tasks.insert_one(completed_task.model_dump())
    test_cases.append(("COMPLETED Task with HTML", completed_id, "/report/task/"))

    # 3. Create a FAILED task
    failed_id = str(uuid.uuid4())
    failed_task = Task(
        task_id=failed_id,
        url="https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id=345678",
        status=TaskStatus.FAILED,
        error="Test error: Something went wrong"
    )
    await db.tasks.insert_one(failed_task.model_dump())
    test_cases.append(("FAILED Task", failed_id, "/report/task/"))

    # 4. Create ANALYZING task (should show loading)
    analyzing_id = str(uuid.uuid4())
    analyzing_task = Task(
        task_id=analyzing_id,
        url="https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id=567890",
        status=TaskStatus.ANALYZING,
        page_name="Analyzing Test"
    )
    await db.tasks.insert_one(analyzing_task.model_dump())
    test_cases.append(("ANALYZING Task", analyzing_id, "/report/task/"))

    # 5. Create COMPLETED policy task with HTML
    policy_completed_id = str(uuid.uuid4())
    policy_completed = PolicyTask(
        task_id=policy_completed_id,
        video_url="https://example.com/video.mp4",
        status=PolicyCheckStatus.COMPLETED,
        html_report="<html><body><h1>Policy Report</h1></body></html>",
        will_pass_moderation=True,
        risk_level="low"
    )
    await db.policy_tasks.insert_one(policy_completed.model_dump())
    test_cases.append(("COMPLETED Policy Task", policy_completed_id, "/report/policy/"))

    # 6. Create CHECKING policy task
    policy_checking_id = str(uuid.uuid4())
    policy_checking = PolicyTask(
        task_id=policy_checking_id,
        video_url="https://example.com/video2.mp4",
        status=PolicyCheckStatus.CHECKING
    )
    await db.policy_tasks.insert_one(policy_checking.model_dump())
    test_cases.append(("CHECKING Policy Task", policy_checking_id, "/report/policy/"))

    # Print test URLs
    base_url = "http://localhost:8000"

    print("📊 Test Cases Created:\n")
    print("=" * 80)

    for i, (description, task_id, endpoint) in enumerate(test_cases, 1):
        full_url = f"{base_url}{endpoint}{task_id}"
        print(f"\n{i}. {description}")
        print(f"   Task ID: {task_id}")
        print(f"   URL: {full_url}")
        print(f"   Expected: ", end="")

        if "PENDING" in description or "ANALYZING" in description or "CHECKING" in description:
            print("Loading page with auto-refresh (202)")
        elif "COMPLETED" in description and "HTML" in description:
            print("HTML report displayed (200)")
        elif "FAILED" in description:
            print("Error page (500)")
        else:
            print("Check manually")

    print("\n" + "=" * 80)

    # Test invalid UUID
    print(f"\n7. Invalid UUID Test")
    print(f"   URL: {base_url}/report/task/invalid-uuid-123")
    print(f"   Expected: Not Found page (404)")

    # Test non-existent task
    non_existent_id = str(uuid.uuid4())
    print(f"\n8. Non-existent Task Test")
    print(f"   URL: {base_url}/report/task/{non_existent_id}")
    print(f"   Expected: Not Found page (404)")

    print("\n" + "=" * 80)
    print("\n✅ Test tasks created successfully!")
    print("\n📝 To test:")
    print("1. Make sure the API is running: uvicorn src.main:app --reload")
    print("2. Open the URLs above in your browser")
    print("3. Verify the expected behavior for each scenario")
    print("\n🧹 Cleanup:")
    print(f"To remove test data, run:")
    print(f"  python -c 'import asyncio; from src.db import MongoDB; asyncio.run(MongoDB.connect()); db = MongoDB.get_db(); asyncio.run(db.tasks.delete_many({{\"task_id\": {{\"$in\": [\"{pending_id}\", \"{completed_id}\", \"{failed_id}\", \"{analyzing_id}\"]}}}}))'")

    # Disconnect
    await MongoDB.disconnect()


if __name__ == "__main__":
    asyncio.run(test_report_viewer())
