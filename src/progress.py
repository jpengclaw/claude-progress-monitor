"""
Progress tracking utilities for Claude Progress Monitor.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional


class ProgressBar:
    """Visual progress bar generator."""
    
    def __init__(self, percentage: int, width: int = 10):
        """
        Initialize progress bar.
        
        Args:
            percentage: Completion percentage (0-100)
            width: Bar width in characters
        """
        self.percentage = max(0, min(100, percentage))
        self.width = width
    
    def render(self) -> str:
        """Render the progress bar as a string."""
        filled = int(self.percentage / 100 * self.width)
        empty = self.width - filled
        return '▰' * filled + '▱' * empty
    
    def __str__(self) -> str:
        return f"{self.render()} {self.percentage}%"


class ProgressTracker:
    """Tracks progress updates over time."""
    
    def __init__(self):
        self.updates: Dict[str, list] = {}
    
    def add_update(self, task_id: str, percentage: int, timestamp: Optional[datetime] = None):
        """
        Record a progress update.
        
        Args:
            task_id: Task identifier
            percentage: Progress percentage
            timestamp: Update timestamp (defaults to now)
        """
        if task_id not in self.updates:
            self.updates[task_id] = []
        
        self.updates[task_id].append({
            'percentage': percentage,
            'timestamp': timestamp or datetime.utcnow()
        })
    
    def get_progress_rate(self, task_id: str) -> float:
        """
        Calculate progress rate (percentage per minute).
        
        Args:
            task_id: Task identifier
            
        Returns:
            Progress rate in %/min
        """
        if task_id not in self.updates or len(self.updates[task_id]) < 2:
            return 0.0
        
        updates = self.updates[task_id]
        first = updates[0]
        last = updates[-1]
        
        time_diff = (last['timestamp'] - first['timestamp']).total_seconds() / 60
        progress_diff = last['percentage'] - first['percentage']
        
        if time_diff == 0:
            return 0.0
        
        return progress_diff / time_diff
    
    def estimate_completion(self, task_id: str) -> Optional[datetime]:
        """
        Estimate completion time based on progress rate.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Estimated completion time or None
        """
        if task_id not in self.updates:
            return None
        
        rate = self.get_progress_rate(task_id)
        if rate <= 0:
            return None
        
        updates = self.updates[task_id]
        current_progress = updates[-1]['percentage']
        remaining = 100 - current_progress
        
        minutes_remaining = remaining / rate
        
        return updates[-1]['timestamp'] + timedelta(minutes=minutes_remaining)
    
    def get_summary(self, task_id: str) -> dict:
        """Get progress summary for a task."""
        if task_id not in self.updates:
            return {
                'updates': 0,
                'current_progress': 0,
                'rate': 0.0,
                'estimated_completion': None
            }
        
        updates = self.updates[task_id]
        
        return {
            'updates': len(updates),
            'current_progress': updates[-1]['percentage'],
            'rate': self.get_progress_rate(task_id),
            'estimated_completion': self.estimate_completion(task_id)
        }
