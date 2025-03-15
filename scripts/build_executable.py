"""
package.py - Enhanced script to package LLM Resume Generator as an executable
"""

import os
import shutil
import subprocess
import sys
import platform
import pkg_resources

def create_directories():
    """Create necessary directories for the build process"""
    print("Creating build directories...")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    os.makedirs("dist", exist_ok=True)
    os.makedirs("build", exist_ok=True)

def build_frontend():
    """Build the React frontend"""
    print("Building frontend...")
    os.chdir("frontend")
    subprocess.run("npm run build", shell=True, check=True)
    os.chdir("..")
    
    # Copy the build to a location the backend can serve
    frontend_build = os.path.join("frontend", "build")
    backend_static = os.path.join("backend", "app", "static")
    
    if os.path.exists(backend_static):
        shutil.rmtree(backend_static)
    
    shutil.copytree(frontend_build, backend_static)
    print("Frontend build complete and copied to backend")

def install_missing_dependencies():
    """Install any missing dependencies required for packaging"""
    print("Checking for missing dependencies...")
    
    # Key dependencies that might be needed
    dependencies = [
        "tzdata",  # For timezone information
        "fontconfig",  # For weasyprint
        "pango",  # For weasyprint
    ]
    
    for dep in dependencies:
        try:
            pkg_resources.get_distribution(dep)
            print(f"✓ {dep} is already installed")
        except pkg_resources.DistributionNotFound:
            print(f"Installing {dep}...")
            subprocess.run(f"pip install {dep}", shell=True)

def build_executable():
    """Package the application with PyInstaller"""
    print("Packaging application with PyInstaller...")
    os.chdir("backend")
    
    # Create a more robust spec file
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Include all required data files
data_files = [
    ('app/static', 'app/static'),
    # Add any other data files your application needs
]

# Collect all required packages
a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=data_files,
    hiddenimports=[
        'uvicorn.logging', 
        'uvicorn.protocols', 
        'uvicorn.lifespan', 
        'uvicorn.protocols.http', 
        'uvicorn.protocols.http.auto',
        'tzdata',
        'email.mime.text',  # Often required by email modules
        'weasyprint',
        'PIL._tkinter_finder',  # Pillow may need this
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Create the PYZ archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LLM_Resume_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False for GUI-only app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Collect all files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LLM_Resume_Generator',
)
"""
    
    with open("resume_generator.spec", "w") as spec_file:
        spec_file.write(spec_content)
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Run PyInstaller with more options
    subprocess.run("pyinstaller resume_generator.spec --clean --log-level=DEBUG", shell=True, check=True)
    os.chdir("..")
    
    # Copy the distribution to the main dist folder
    backend_dist = os.path.join("backend", "dist", "LLM_Resume_Generator")
    if os.path.exists(os.path.join("dist", "LLM_Resume_Generator")):
        shutil.rmtree(os.path.join("dist", "LLM_Resume_Generator"))
    shutil.copytree(backend_dist, os.path.join("dist", "LLM_Resume_Generator"))
    
    print("Executable packaging complete")

def create_config_script():
    """Create an improved configuration script for setting API keys"""
    print("Creating configuration script...")
    
    config_script = """
@echo off
echo LLM Resume Generator Configuration
echo ===============================
echo.
set /p GEMINI_API_KEY="Enter your Gemini API key: "
set /p UNSPLASH_API_KEY="Enter your Unsplash API key: "

echo.
echo Writing configuration...
echo GEMINI_API_KEY=%GEMINI_API_KEY% > config.env
echo UNSPLASH_API_KEY=%UNSPLASH_API_KEY% >> config.env
echo.
echo Configuration complete! You can now run LLM_Resume_Generator using start_app.bat
echo.
echo Press any key to exit...
pause > nul
"""
    with open(os.path.join("dist", "LLM_Resume_Generator", "configure.bat"), "w") as f:
        f.write(config_script)
    
    # Also create a clearer README
    readme = """
# LLM Resume Generator

## Setup Instructions

1. Run `configure.bat` first to set up your API keys
2. Run `start_app.bat` to launch the application
3. Open your browser and navigate to http://localhost:8000

## Troubleshooting

If the application doesn't start:
- Check that your API keys are correct
- Ensure no other application is using port 8000
- Try running with debug mode by using `debug_mode.bat`

## Support

If you encounter issues, please report them at:
https://github.com/eleven-day/cv_generator/issues
"""
    with open(os.path.join("dist", "LLM_Resume_Generator", "README.txt"), "w") as f:
        f.write(readme)
    
    print("Configuration script created")

def create_launcher():
    """Create an improved launcher script that loads environment variables"""
    print("Creating launcher script...")
    
    launcher_script = """
@echo off
echo Loading configuration...
for /F "tokens=*" %%A in (config.env) do set %%A
echo.
echo Starting LLM Resume Generator...
echo The application will be available at http://localhost:8000
echo.
echo Press Ctrl+C to stop the server when you're done
echo.
start http://localhost:8000
LLM_Resume_Generator.exe
"""
    with open(os.path.join("dist", "LLM_Resume_Generator", "start_app.bat"), "w") as f:
        f.write(launcher_script)
    
    # Add a debug mode launcher
    debug_script = """
@echo off
echo Loading configuration...
for /F "tokens=*" %%A in (config.env) do set %%A
echo.
echo Starting LLM Resume Generator in DEBUG mode...
echo The application will be available at http://localhost:8000
echo.
echo Press Ctrl+C to stop the server when you're done
echo.
set PYTHONUNBUFFERED=1
start http://localhost:8000
LLM_Resume_Generator.exe --debug
pause
"""
    with open(os.path.join("dist", "LLM_Resume_Generator", "debug_mode.bat"), "w") as f:
        f.write(debug_script)
    
    print("Launcher scripts created")

def create_test_script():
    """Create a test script to verify the packaged app works"""
    print("Creating test script...")
    
    test_script = """
@echo off
echo Testing LLM Resume Generator...
echo.
echo This script will:
echo 1. Check that all required files exist
echo 2. Verify the application can start
echo 3. Test API key configuration
echo.
echo Press any key to begin testing...
pause > nul

echo Checking for required files...
if not exist LLM_Resume_Generator.exe (
    echo ERROR: Executable file not found!
    goto :error
)
if not exist app (
    echo ERROR: Application files not found!
    goto :error
)
echo All required files found.
echo.

echo Testing executable...
LLM_Resume_Generator.exe --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Executable test failed!
    goto :error
)
echo Executable test passed.
echo.

echo All tests completed successfully!
goto :end

:error
echo.
echo Test failed! Please check the errors above.
pause
exit /b 1

:end
echo.
echo Press any key to exit...
pause > nul
exit /b 0
"""
    with open(os.path.join("dist", "LLM_Resume_Generator", "test_app.bat"), "w") as f:
        f.write(test_script)
    
    print("Test script created")

def copy_backend_requirements():
    """Copy backend requirements file for reference"""
    print("Copying backend requirements...")
    shutil.copy(
        os.path.join("backend", "requirements.txt"),
        os.path.join("dist", "LLM_Resume_Generator", "requirements.txt")
    )

def main():
    """Main packaging function with enhanced checks"""
    print("Starting enhanced packaging process for LLM Resume Generator...")
    
    # Ensure we're in the project root
    if not (os.path.exists("frontend") and os.path.exists("backend")):
        print("Error: Script must be run from the project root directory")
        sys.exit(1)
    
    try:
        create_directories()
        install_missing_dependencies()
        build_frontend()
        build_executable()
        create_config_script()
        create_launcher()
        create_test_script()
        copy_backend_requirements()
        
        print("\nPackaging complete!")
        print("The executable package is available in: dist/LLM_Resume_Generator/")
        print("1. Run 'test_app.bat' to verify the application works")
        print("2. Run 'configure.bat' to set your API keys")
        print("3. Run 'start_app.bat' to launch the application")
    
    except Exception as e:
        print(f"Error during packaging: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()