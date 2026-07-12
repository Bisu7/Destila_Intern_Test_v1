import subprocess
import os
import sys

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(root_dir, 'frontend')

    print("Starting FastAPI backend...")
    # Start backend from the root directory so 'backend.main:app' resolves correctly
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"],
        cwd=root_dir
    )

    print("Starting Vite frontend...")
    # Start frontend from the frontend directory
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        shell=True
    )

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
