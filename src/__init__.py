"""
Claude Progress Monitor

A Python library for monitoring Claude subagent/tool execution with automatic
progress tracking and status updates.

Usage:
    from claude_progress_monitor import Monitor, spawn_with_monitoring
    
    monitor = Monitor()
    result = await monitor.spawn_with_monitoring(
        task="Research AI topic",
        tools=["web_search", "calculator"],
        timeout=300
    )
"""

__version__ = "1.0.0"
__author__ = "Operational Neural Network"

from .monitor import Monitor, spawn_with_monitoring
from .progress import ProgressTracker, ProgressBar
from .exceptions import TimeoutError, SubagentError

__all__ = [
    'Monitor',
    'spawn_with_monitoring',
    'ProgressTracker',
    'ProgressBar',
    'TimeoutError',
    'SubagentError'
]
