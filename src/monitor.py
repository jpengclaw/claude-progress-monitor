"""
Claude Progress Monitor - Core Module

Provides monitoring capabilities for Claude subagent execution with automatic
progress tracking and status updates.
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass, field
import logging

from .progress import ProgressTracker, ProgressBar
from .exceptions import TimeoutError, SubagentError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SubagentTask:
    """Represents a subagent task being monitored."""
    task_id: str
    description: str
    start_time: datetime
    timeout: int  # seconds
    tools: List[str] = field(default_factory=list)
    status: str = "running"  # running, completed, failed, timeout
    progress: int = 0  # 0-100
    last_update: datetime = field(default_factory=datetime.utcnow)
    check_interval: int = 60  # seconds
    next_check: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=1))


class Monitor:
    """
    Monitors Claude subagent execution with automatic progress tracking.
    
    Usage:
        monitor = Monitor(update_interval=90)
        result = await monitor.spawn_with_monitoring(
            task="Research AI topic",
            tools=["web_search"],
            timeout=300
        )
    """
    
    def __init__(self, update_interval: int = 90, timeout_threshold: int = 900):
        """
        Initialize the monitor.
        
        Args:
            update_interval: Seconds between progress updates (default: 90)
            timeout_threshold: Seconds before considering task stuck (default: 900 = 15 min)
        """
        self.update_interval = update_interval
        self.timeout_threshold = timeout_threshold
        self.active_tasks: Dict[str, SubagentTask] = {}
        self.progress_tracker = ProgressTracker()
        self._running = False
        self._monitor_task = None
        
    async def spawn_with_monitoring(
        self,
        task: str,
        tools: List[str],
        timeout: int = 300,
        task_id: Optional[str] = None,
        on_progress: Optional[Callable[[str, int], None]] = None,
        on_complete: Optional[Callable[[str, Any], None]] = None,
        on_error: Optional[Callable[[str, Exception], None]] = None
    ) -> Any:
        """
        Spawn a Claude subagent with automatic progress monitoring.
        
        Args:
            task: Task description for the subagent
            tools: List of tools to provide to the subagent
            timeout: Maximum time to wait in seconds
            task_id: Optional unique task identifier
            on_progress: Callback for progress updates (task_id, percentage)
            on_complete: Callback on completion (task_id, result)
            on_error: Callback on error (task_id, exception)
            
        Returns:
            Task result
            
        Raises:
            TimeoutError: If task exceeds timeout
            SubagentError: If subagent fails
        """
        
        task_id = task_id or f"task_{int(time.time())}"
        
        # Create task record
        subagent_task = SubagentTask(
            task_id=task_id,
            description=task,
            start_time=datetime.utcnow(),
            timeout=timeout,
            tools=tools,
            check_interval=60
        )
        
        self.active_tasks[task_id] = subagent_task
        
        logger.info(f"✅ Spawned subagent: {task_id}")
        print(f"✅ Task '{task_id}' started. Will update every {self.update_interval}s.")
        
        try:
            # Start monitoring
            result = await self._execute_with_monitoring(
                subagent_task,
                on_progress,
                on_complete,
                on_error
            )
            
            subagent_task.status = "completed"
            subagent_task.progress = 100
            
            if on_complete:
                on_complete(task_id, result)
            
            logger.info(f"✅ Task completed: {task_id}")
            print(f"✅ Task '{task_id}' completed!")
            
            return result
            
        except asyncio.TimeoutError:
            subagent_task.status = "timeout"
            logger.error(f"❌ Task timed out: {task_id}")
            print(f"❌ Task '{task_id}' timed out after {timeout}s")
            
            if on_error:
                on_error(task_id, TimeoutError(f"Task {task_id} timed out"))
            
            raise TimeoutError(f"Task {task_id} exceeded timeout of {timeout}s")
            
        except Exception as e:
            subagent_task.status = "failed"
            logger.error(f"❌ Task failed: {task_id} - {e}")
            print(f"❌ Task '{task_id}' failed: {e}")
            
            if on_error:
                on_error(task_id, e)
            
            raise SubagentError(f"Task {task_id} failed: {e}")
            
        finally:
            # Cleanup
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
    
    async def _execute_with_monitoring(
        self,
        task: SubagentTask,
        on_progress: Optional[Callable],
        on_complete: Optional[Callable],
        on_error: Optional[Callable]
    ) -> Any:
        """
        Execute task with progress monitoring.
        
        This simulates the actual Claude subagent execution.
        In real usage, this would call Claude's API.
        """
        
        start_time = time.time()
        last_update = start_time
        
        # Simulate task execution with progress updates
        # In real implementation, this would integrate with Claude's API
        while True:
            elapsed = time.time() - start_time
            
            # Check for timeout
            if elapsed > task.timeout:
                raise asyncio.TimeoutError()
            
            # Simulate progress (in real use, this comes from Claude)
            task.progress = min(100, int((elapsed / task.timeout) * 100 * 2))
            task.last_update = datetime.utcnow()
            
            # Send progress update every update_interval seconds
            if time.time() - last_update >= self.update_interval:
                self._send_progress_update(task, on_progress)
                last_update = time.time()
            
            # Check if task is complete (simulate completion at 100%)
            if task.progress >= 100:
                return {"status": "success", "task_id": task.task_id, "result": "Task completed"}
            
            # Sleep before next check
            await asyncio.sleep(5)
    
    def _send_progress_update(
        self,
        task: SubagentTask,
        on_progress: Optional[Callable]
    ):
        """Send progress update to user."""
        
        progress_bar = ProgressBar(task.progress)
        bar_display = progress_bar.render()
        
        message = f"""
📊 Progress Update

Task: {task.task_id}
Status: {task.status}
Progress: {bar_display} {task.progress}%
Elapsed: {int((datetime.utcnow() - task.start_time).total_seconds() / 60)}m
"""
        
        print(message)
        
        if on_progress:
            on_progress(task.task_id, task.progress)
    
    def check_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Check status of a specific task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task status dict or None if not found
        """
        if task_id not in self.active_tasks:
            return None
        
        task = self.active_tasks[task_id]
        return {
            "task_id": task.task_id,
            "status": task.status,
            "progress": task.progress,
            "elapsed": int((datetime.utcnow() - task.start_time).total_seconds()),
            "description": task.description
        }
    
    def kill_task(self, task_id: str) -> bool:
        """
        Kill a running task.
        
        Args:
            task_id: Task to kill
            
        Returns:
            True if killed successfully
        """
        if task_id not in self.active_tasks:
            logger.warning(f"Task {task_id} not found")
            return False
        
        task = self.active_tasks[task_id]
        task.status = "killed"
        
        logger.info(f"🛑 Killed task: {task_id}")
        print(f"🛑 Task '{task_id}' killed")
        
        return True
    
    def list_active_tasks(self) -> List[Dict[str, Any]]:
        """List all active tasks."""
        return [
            {
                "task_id": task.task_id,
                "status": task.status,
                "progress": task.progress,
                "elapsed": int((datetime.utcnow() - task.start_time).total_seconds())
            }
            for task in self.active_tasks.values()
        ]


# Convenience function for simple usage
async def spawn_with_monitoring(
    task: str,
    tools: List[str],
    timeout: int = 300,
    **kwargs
) -> Any:
    """
    Convenience function to spawn and monitor a task.
    
    Args:
        task: Task description
        tools: Tools to provide
        timeout: Timeout in seconds
        **kwargs: Additional arguments passed to Monitor.spawn_with_monitoring
        
    Returns:
        Task result
    """
    monitor = Monitor()
    return await monitor.spawn_with_monitoring(task, tools, timeout, **kwargs)
