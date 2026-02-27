# Claude Progress Monitor

A Python library for monitoring Claude subagent execution with automatic progress tracking and status updates.

## Overview

This library solves the problem of silent subagent failures in Claude-based AI systems. It implements automatic progress monitoring with configurable update intervals, timeout handling, and graceful error recovery.

## Features

- **Automatic Progress Tracking**: Monitors subagent execution with configurable intervals
- **90-Second Update Rule**: Sends progress updates every 90 seconds by default
- **15-Minute Timeout**: Auto-detects stuck tasks after 15 minutes
- **Visual Progress Bars**: Displays progress with visual indicators
- **Async/Await Support**: Full async support for modern Python applications
- **Callback System**: Hooks for progress, completion, and error events
- **Task Management**: List, check, and kill active tasks

## Installation

### Via pip (when published)

```bash
pip install claude-progress-monitor
```

### Manual Installation

```bash
git clone https://github.com/jpengclaw/claude-progress-monitor.git
cd claude-progress-monitor
pip install -e .
```

## Quick Start

```python
import asyncio
from claude_progress_monitor import Monitor, spawn_with_monitoring

async def main():
    # Simple usage
    result = await spawn_with_monitoring(
        task="Research AI energy consumption",
        tools=["web_search", "calculator"],
        timeout=300
    )
    print(result)

# Run
asyncio.run(main())
```

## Advanced Usage

```python
import asyncio
from claude_progress_monitor import Monitor

async def main():
    monitor = Monitor(update_interval=90, timeout_threshold=900)
    
    # Define callbacks
    def on_progress(task_id, percentage):
        print(f"Task {task_id}: {percentage}%")
    
    def on_complete(task_id, result):
        print(f"Task {task_id} completed: {result}")
    
    def on_error(task_id, error):
        print(f"Task {task_id} failed: {error}")
    
    # Spawn with monitoring
    result = await monitor.spawn_with_monitoring(
        task="Complex research task",
        tools=["web_search", "code_interpreter"],
        timeout=600,
        task_id="research-001",
        on_progress=on_progress,
        on_complete=on_complete,
        on_error=on_error
    )

asyncio.run(main())
```

## Configuration

```python
from claude_progress_monitor import Monitor

# Create monitor with custom settings
monitor = Monitor(
    update_interval=90,      # Progress updates every 90 seconds
    timeout_threshold=900    # 15-minute timeout
)
```

## Progress Tracking

```python
from claude_progress_monitor import ProgressTracker, ProgressBar

# Create progress bar
bar = ProgressBar(60)
print(bar)  # Output: ▰▰▰▰▰▰▱▱▱▱ 60%

# Track progress over time
tracker = ProgressTracker()
tracker.add_update("task-001", 25)
tracker.add_update("task-001", 50)
tracker.add_update("task-001", 75)

# Get progress rate
rate = tracker.get_progress_rate("task-001")
print(f"Progress rate: {rate:.1f}%/min")

# Estimate completion
eta = tracker.estimate_completion("task-001")
print(f"Estimated completion: {eta}")
```

## Task Management

```python
from claude_progress_monitor import Monitor

monitor = Monitor()

# List active tasks
tasks = monitor.list_active_tasks()
for task in tasks:
    print(f"{task['task_id']}: {task['progress']}%")

# Check specific task
status = monitor.check_task("task-001")
if status:
    print(f"Status: {status['status']}, Progress: {status['progress']}%")

# Kill stuck task
monitor.kill_task("task-001")
```

## The 90-Second Rule

This library implements the "90-Second Rule" for progress updates:

| Time | Action |
|------|--------|
| 0s | Spawn subagent, start monitoring |
| 90s | Send progress update (if running) |
| 180s | Send progress update (if running) |
| 270s | Send progress update (if running) |
| Completion | Notify immediately |
| Failure | Notify immediately |

This frequency balances:
- **User awareness**: Regular updates prevent anxiety
- **Efficiency**: Not so frequent as to be annoying
- **Trust**: Consistent communication builds confidence

## Error Handling

```python
from claude_progress_monitor import Monitor, TimeoutError, SubagentError

monitor = Monitor()

try:
    result = await monitor.spawn_with_monitoring(
        task="Long running task",
        tools=["web_search"],
        timeout=300
    )
except TimeoutError:
    print("Task exceeded timeout - took over 5 minutes")
except SubagentError as e:
    print(f"Task failed: {e}")
```

## Integration with Claude API

```python
import anthropic
from claude_progress_monitor import Monitor

# Initialize Claude client
client = anthropic.Anthropic()

# Create monitor
monitor = Monitor()

# Use with Claude
async def run_with_claude():
    # This would integrate with actual Claude API
    result = await monitor.spawn_with_monitoring(
        task="Analyze dataset",
        tools=["code_interpreter"],
        timeout=600
    )
    return result
```

## Examples

See the `examples/` directory for complete working examples:

- `basic_usage.py` - Simple monitoring setup
- `advanced_callbacks.py` - Using callbacks
- `multiple_tasks.py` - Managing multiple concurrent tasks
- `integration_example.py` - Integration with Claude API

## Documentation

- [API Reference](docs/api.md)
- [Configuration Guide](docs/config.md)
- [Best Practices](docs/best_practices.md)

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=claude_progress_monitor tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- Issues: https://github.com/jpengclaw/claude-progress-monitor/issues
- Discussions: GitHub Discussions

---

**Built by Operational Neural Network** | Making AI agents self-sustaining
