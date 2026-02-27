"""
Custom exceptions for Claude Progress Monitor.
"""


class TimeoutError(Exception):
    """Raised when a subagent task exceeds its timeout."""
    
    def __init__(self, message: str = "Task exceeded timeout"):
        self.message = message
        super().__init__(self.message)


class SubagentError(Exception):
    """Raised when a subagent task fails."""
    
    def __init__(self, message: str = "Subagent task failed"):
        self.message = message
        super().__init__(self.message)


class MonitoringError(Exception):
    """Raised when monitoring system encounters an error."""
    
    def __init__(self, message: str = "Monitoring system error"):
        self.message = message
        super().__init__(self.message)
