import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path

def build_executable(output_dir, app_name="Resume Generator"):
    """
    Build an executable from the Python FastAPI backend and React frontend
    
    Args:
        output_dir: Directory where the executable will be created
        app_name: Name of the application
    """
    print(f"Building {app_name} executable...")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Install dependencies if needed
    print("Checking dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
    
    # Install pyinstaller if not already installed
    try:
        import pyinstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"], check=True)
    
    # Step 1: Build the React frontend
    print("Building frontend...")
    os.chdir("frontend")
    if not os.path.exists("node_modules"):
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], check=True)
    subprocess.run(["npm", "run", "build"], check=True)
    os.chdir("..")
    
    # Step 2: Create a directory structure for PyInstaller
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Copy the built frontend to the static folder in backend
    static_dir = Path("backend/app/static")
    if static_dir.exists():
        shutil.rmtree(static_dir)
    static_dir.mkdir(parents=True)
    shutil.copytree("frontend/build", static_dir, dirs_exist_ok=True)
    
    # Step 3: Create a combined script that runs both backend and frontend
    entry_point = build_dir / "resume_generator.py"
    with open(entry_point, "w") as f:
        f.write("""
import os
import sys
import uvicorn
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    # Open browser after a short delay
    Timer(2, open_browser).start()
    
    # Run the FastAPI app
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from backend.app.main import app
    uvicorn.run(app, host="0.0.0.0", port=8000)
""")
    
    # Step 4: Use PyInstaller to create the executable
    print("Building executable with PyInstaller...")
    os.chdir("build")
    
    # Make sure we include all necessary packages
    # Find the favicon if it exists
    favicon_path = None
    if os.path.exists("../frontend/public/favicon.ico"):
        favicon_path = "../frontend/public/favicon.ico"
    
    pyinstaller_cmd = [
        "pyinstaller",
        "--name", app_name,
        "--onefile",
        "--windowed" if sys.platform != "linux" else "--console",
        "--add-data", f"../backend/app/static{os.pathsep}app/static",
    ]
    
    # Add favicon if available
    if favicon_path:
        pyinstaller_cmd.extend(["--icon", favicon_path])
    
    pyinstaller_cmd.append("resume_generator.py")
    
    subprocess.run(pyinstaller_cmd, check=True)
    os.chdir("..")
    
    # Step 5: Copy the executable to the output directory
    dist_dir = Path("build/dist")
    exe_name = f"{app_name}.exe" if sys.platform == "win32" else app_name
    executable = dist_dir / exe_name
    
    if executable.exists():
        shutil.copy(executable, output_path)
        print(f"Executable built successfully: {output_path / exe_name}")
    else:
        print(f"Error: Executable not found at {executable}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Resume Generator executable")
    parser.add_argument("--output", default="dist", help="Output directory for the executable")
    parser.add_argument("--name", default="Resume Generator", help="Name of the application")
    
    args = parser.parse_args()
    build_executable(args.output, args.name)