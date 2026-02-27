"""
Basic usage example for Claude Progress Monitor.

Shows the simplest way to monitor a subagent task.
"""

import asyncio
from claude_progress_monitor import spawn_with_monitoring


async def main():
    """Basic monitoring example."""
    
    print("🚀 Starting basic monitoring example\n")
    
    # Simple usage - spawn and monitor
    result = await spawn_with_monitoring(
        task="Research renewable energy trends",
        tools=["web_search", "calculator"],
        timeout=300,  # 5 minute timeout
        task_id="research-001"
    )
    
    print(f"\n✅ Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
