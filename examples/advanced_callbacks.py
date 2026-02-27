"""
Advanced example with callbacks for Claude Progress Monitor.

Shows how to use progress, completion, and error callbacks.
"""

import asyncio
from claude_progress_monitor import Monitor


async def main():
    """Advanced monitoring with callbacks."""
    
    print("🚀 Starting advanced monitoring example\n")
    
    # Create monitor with custom settings
    monitor = Monitor(
        update_interval=90,  # Update every 90 seconds
        timeout_threshold=900  # 15 minute timeout
    )
    
    # Define callbacks
    def on_progress(task_id: str, percentage: int):
        """Called every 90 seconds with progress update."""
        print(f"📊 Task {task_id} progress: {percentage}%")
    
    def on_complete(task_id: str, result):
        """Called when task completes successfully."""
        print(f"✅ Task {task_id} completed!")
        print(f"   Result: {result}")
    
    def on_error(task_id: str, error: Exception):
        """Called when task fails."""
        print(f"❌ Task {task_id} failed: {error}")
    
    # Spawn task with monitoring and callbacks
    try:
        result = await monitor.spawn_with_monitoring(
            task="Complex data analysis",
            tools=["code_interpreter", "web_search", "file_reader"],
            timeout=600,  # 10 minutes
            task_id="analysis-001",
            on_progress=on_progress,
            on_complete=on_complete,
            on_error=on_error
        )
        
        print(f"\n🎉 Final result: {result}")
        
    except Exception as e:
        print(f"\n💥 Unhandled error: {e}")
    
    # List all active tasks (should be empty now)
    active_tasks = monitor.list_active_tasks()
    print(f"\n📋 Active tasks: {len(active_tasks)}")


if __name__ == "__main__":
    asyncio.run(main())
