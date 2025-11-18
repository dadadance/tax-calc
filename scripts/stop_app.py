#!/usr/bin/env python3
"""Script to stop the Streamlit tax calculator app."""
import sys
import os
import signal
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

APP_DIR = Path(__file__).parent.parent
PID_FILE = APP_DIR / ".streamlit.pid"


def stop_app():
    """Stop the Streamlit app."""
    if not PID_FILE.exists():
        print("ℹ️  No app is currently running (no PID file found)")
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
    except (ValueError, FileNotFoundError):
        print("ℹ️  Invalid PID file")
        PID_FILE.unlink()
        return False
    
    # Check if process exists
    try:
        os.kill(pid, 0)  # Signal 0 doesn't kill, just checks
    except OSError:
        print(f"ℹ️  Process {pid} is not running (stale PID file)")
        PID_FILE.unlink()
        return False
    
    # Try to stop gracefully
    try:
        print(f"🛑 Stopping app (PID: {pid})...")
        
        # Send SIGTERM (graceful shutdown)
        os.kill(pid, signal.SIGTERM)
        
        # Wait a bit for graceful shutdown
        import time
        time.sleep(2)
        
        # Check if still running
        try:
            os.kill(pid, 0)
            # Still running, force kill
            print("   Process didn't stop gracefully, forcing shutdown...")
            os.kill(pid, signal.SIGKILL)
            time.sleep(1)
        except OSError:
            # Process stopped
            pass
        
        # Remove PID file
        if PID_FILE.exists():
            PID_FILE.unlink()
        
        print("✓ App stopped successfully")
        return True
        
    except ProcessLookupError:
        print(f"ℹ️  Process {pid} already stopped")
        PID_FILE.unlink()
        return True
    except PermissionError:
        print(f"❌ Permission denied. Try: sudo kill {pid}")
        return False
    except Exception as e:
        print(f"❌ Error stopping app: {e}")
        return False


def kill_by_port(port=8501):
    """Kill process by port (fallback method)."""
    import subprocess
    
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split('\n'):
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if len(parts) > 4:
                        pid = parts[-1]
                        subprocess.run(["taskkill", "/F", "/PID", pid])
                        print(f"✓ Killed process on port {port}")
                        return True
        else:
            # Unix-like
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                pid = result.stdout.strip()
                os.kill(int(pid), signal.SIGTERM)
                print(f"✓ Killed process {pid} on port {port}")
                return True
    except Exception as e:
        print(f"⚠️  Could not kill by port: {e}")
    
    return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Stop the Georgian Tax Calculator app")
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8501,
        help="Port to check/kill (default: 8501)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force kill by port (if PID file method fails)"
    )
    
    args = parser.parse_args()
    
    success = stop_app()
    
    if not success and args.force:
        print(f"\nTrying to kill process on port {args.port}...")
        kill_by_port(args.port)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

