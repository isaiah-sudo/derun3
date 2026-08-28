"""
CyberSurge 3D - Standalone EXE Builder
Uses PyInstaller to package Python, Ursina Engine, and Panda3D assets into a standalone Windows executable.
"""
import os
import sys
import subprocess
import shutil

def build():
    print("========================================")
    print("  CyberSurge 3D - Standalone EXE Build  ")
    print("========================================")

    # 1. Ensure PyInstaller is installed
    try:
        import PyInstaller
        print(f"[OK] Found PyInstaller version {PyInstaller.__version__}")
    except ImportError:
        print("[INFO] Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Configure build arguments
    # --collect-all collects all Panda3D DLLs, display pipes (OpenGL/DirectX), and Ursina internal models
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=CyberSurge3D",
        "--noconfirm",
        "--clean",
        "--windowed",  # No black terminal window behind game
        "--collect-all=ursina",
        "--collect-all=direct",
        "--collect-all=panda3d",
        "--add-data=game;game",
        "main.py"
    ]

    # Check for optional icon
    if os.path.exists("assets/icon.ico"):
        cmd.insert(4, "--icon=assets/icon.ico")

    print(f"\n[BUILD] Running PyInstaller command...")
    print(" ".join(cmd))
    print("-" * 50)

    try:
        subprocess.check_call(cmd)
        print("-" * 50)
        print("\n[SUCCESS] Build completed successfully!")
        
        exe_path = os.path.abspath(os.path.join("dist", "CyberSurge3D", "CyberSurge3D.exe"))
        if os.path.exists(exe_path):
            print(f"\n[OUTPUT] Executable created at:")
            print(f"  --> {exe_path}")
            print("\nYou can run the game directly or distribute the 'dist/CyberSurge3D' folder!")
        else:
            print("\n[OUTPUT] Check the 'dist' folder for your executable.")
            
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Build failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    build()
