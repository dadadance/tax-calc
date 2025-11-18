"""Error logging system for the tax calculator app."""
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json


# Create errors directory
ERRORS_DIR = Path(__file__).parent.parent / "errors"
ERRORS_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = ERRORS_DIR / "app_errors.log"
JSON_LOG_FILE = ERRORS_DIR / "errors.jsonl"  # JSON Lines format for easier parsing


class ErrorLogger:
    """Centralized error logging system."""
    
    def __init__(self):
        """Initialize the logger."""
        self.logger = logging.getLogger("tax_calc")
        self.logger.setLevel(logging.ERROR)
        
        # File handler for text logs
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(pathname)s:%(lineno)d\n'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def log_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_action: Optional[str] = None
    ) -> str:
        """
        Log an error with context.
        
        Args:
            error: The exception that occurred
            context: Additional context dictionary
            user_action: Description of what the user was doing
            
        Returns:
            Error ID for tracking
        """
        error_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        timestamp = datetime.now().isoformat()
        
        # Get full traceback
        tb_str = traceback.format_exc()
        
        # Prepare error data
        error_data = {
            "error_id": error_id,
            "timestamp": timestamp,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "user_action": user_action or "Unknown",
            "context": context or {},
            "traceback": tb_str
        }
        
        # Log to text file
        error_msg = f"Error ID: {error_id}\n"
        error_msg += f"User Action: {user_action or 'Unknown'}\n"
        error_msg += f"Context: {json.dumps(context, indent=2, default=str)}\n"
        error_msg += f"Error: {type(error).__name__}: {str(error)}\n"
        error_msg += f"Traceback:\n{tb_str}\n"
        error_msg += "=" * 80 + "\n"
        
        self.logger.error(error_msg)
        
        # Log to JSON file (append mode)
        try:
            with open(JSON_LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(error_data, default=str) + '\n')
        except Exception as e:
            # Fallback if JSON logging fails
            self.logger.error(f"Failed to write JSON log: {e}")
        
        return error_id
    
    def get_recent_errors(self, limit: int = 100) -> list:
        """Get recent errors from JSON log file."""
        errors = []
        if not JSON_LOG_FILE.exists():
            return errors
        
        try:
            with open(JSON_LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Read last N lines
                for line in lines[-limit:]:
                    try:
                        error_data = json.loads(line.strip())
                        errors.append(error_data)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            self.logger.error(f"Failed to read JSON log: {e}")
        
        return list(reversed(errors))  # Most recent first
    
    def clear_logs(self):
        """Clear all log files."""
        try:
            if LOG_FILE.exists():
                LOG_FILE.unlink()
            if JSON_LOG_FILE.exists():
                JSON_LOG_FILE.unlink()
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear logs: {e}")
            return False
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Get statistics about logged errors."""
        stats = {
            "total_errors": 0,
            "errors_by_type": {},
            "errors_by_action": {},
            "latest_error": None
        }
        
        errors = self.get_recent_errors(limit=10000)  # Get all
        stats["total_errors"] = len(errors)
        
        for error in errors:
            # Count by type
            error_type = error.get("error_type", "Unknown")
            stats["errors_by_type"][error_type] = stats["errors_by_type"].get(error_type, 0) + 1
            
            # Count by action
            action = error.get("user_action", "Unknown")
            stats["errors_by_action"][action] = stats["errors_by_action"].get(action, 0) + 1
        
        if errors:
            stats["latest_error"] = errors[0]
        
        return stats


# Global logger instance
logger = ErrorLogger()


def log_app_error(error: Exception, user_action: str = None, **context):
    """
    Convenience function to log app errors.
    
    Args:
        error: The exception
        user_action: What the user was doing
        **context: Additional context as keyword arguments
    """
    return logger.log_error(error, context=context, user_action=user_action)

