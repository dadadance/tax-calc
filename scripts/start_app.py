#!/usr/bin/env python3
"""Script to start the Streamlit tax calculator app."""
import sys
import subprocess
import os
import signal
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

APP_DIR = Path(__file__).parent.parent
PID_FILE = APP_DIR / ".streamlit.pid"
PORT = 8501


def is_app_running():
    """Check if the app is already running."""
    if not PID_FILE.exists():
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process exists
        try:
            os.kill(pid, 0)  # Signal 0 doesn't kill, just checks if process exists
            return True
        except OSError:
            # Process doesn't exist, remove stale PID file
            PID_FILE.unlink()
            return False
    except (ValueError, FileNotFoundError):
        return False


def start_app(port=None, headless=False):
    """Start the Streamlit app."""
    if port is None:
        port = PORT
    
    if is_app_running():
        print(f"⚠️  App is already running on port {port}")
        print("   Use 'stop_app.py' to stop it first, or use a different port")
        return False
    
    app_file = APP_DIR / "app.py"
    if not app_file.exists():
        print(f"❌ Error: {app_file} not found!")
        return False
    
    print(f"🚀 Starting Georgian Tax Calculator...")
    print(f"   Port: {port}")
    print(f"   App: {app_file}")
    
    # Build command
    cmd = ["uv", "run", "streamlit", "run", str(app_file), "--server.port", str(port)]
    
    if headless:
        cmd.extend(["--server.headless", "true"])
    
    try:
        # Start process
        process = subprocess.Popen(
            cmd,
            cwd=str(APP_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True  # Detach from parent process
        )
        
        # Save PID
        with open(PID_FILE, 'w') as f:
            f.write(str(process.pid))
        
        print(f"✓ App started successfully!")
        print(f"   PID: {process.pid}")
        print(f"   URL: http://localhost:{port}")
        print(f"\n   To stop the app, run: uv run python scripts/stop_app.py")
        print(f"   Or: kill {process.pid}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        if PID_FILE.exists():
            PID_FILE.unlink()
        return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start the Georgian Tax Calculator app")
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=PORT,
        help=f"Port to run on (default: {PORT})"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (no browser)"
    )
    parser.add_argument(
        "--background",
        action="store_true",
        help="Run in background (detached)"
    )
    
    args = parser.parse_args()
    
    if args.background:
        # Run in background
        import sys
        if sys.platform != "win32":
            # Fork on Unix-like systems
            pid = os.fork()
            if pid == 0:
                # Child process
                os.setsid()
                start_app(port=args.port, headless=args.headless)
                sys.exit(0)
            else:
                # Parent process
                print(f"Started app in background (PID: {pid})")
        else:
            # Windows - just start normally
            start_app(port=args.port, headless=args.headless)
    else:
        # Run in foreground
        success = start_app(port=args.port, headless=args.headless)
        if success:
            print("\n📝 App is running. Press Ctrl+C to stop.")
            try:
                # Wait for process
                import time
                while True:
                    if not is_app_running():
                        print("\n⚠️  App stopped unexpectedly")
                        break
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nStopping app...")
                stop_app()
        sys.exit(0 if success else 1)


def stop_app():
    """Stop the app (helper function)."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.stop_app import stop_app as stop
    return stop()


if __name__ == "__main__":
    main()

