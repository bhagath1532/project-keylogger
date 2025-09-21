#!/usr/bin/env python3
# KEYLOGGER DETECTION PROJECT - ENVIRONMENT SETUP
# EDUCATIONAL USE ONLY – run in lab VMs with permission

import os, sys, subprocess, platform
from pathlib import Path

def run_command(command, desc):
    print(f"[INFO] {desc}...")
    try:
        subprocess.run(command, shell=True, check=True,
                       capture_output=True, text=True)
        print(f"[SUCCESS] {desc}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {desc} failed: {e.stderr}")
        return False

def check_python():
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 8):
        print(f"[ERROR] Python 3.8+ required (found {v.major}.{v.minor})")
        return False
    print(f"[INFO] Python {v.major}.{v.minor}.{v.micro} OK")
    return True

def create_venv():
    name = "keylogger-env"
    if Path(name).exists():
        print(f"[INFO] Virtual env '{name}' already exists")
        return name
    return name if run_command(f"python -m venv {name}", "Creating venv") else None

def install_deps(venv):
    pip = f"{venv}\\Scripts\\pip" if platform.system()=="Windows" else f"{venv}/bin/pip"
    run_command(f"{pip} install --upgrade pip", "Upgrading pip")
    if Path("requirements.txt").exists():
        run_command(f"{pip} install -r requirements.txt", "Installing dependencies")
    else:
        for dep in ["pynput>=1.7.6", "lxml>=4.9.0", "python-evtx>=0.7.4"]:
            run_command(f"{pip} install {dep}", f"Installing {dep}")

def make_dirs():
    for d in ["logs","reports","test_data"]:
        Path(d).mkdir(exist_ok=True)
        print(f"[INFO] Created {d}")

def usage(venv):
    act = f"{venv}\\Scripts\\activate" if platform.system()=="Windows" else f"source {venv}/bin/activate"
    print("\n" + "="*50)
    print("SETUP COMPLETE - EDUCATIONAL USE ONLY")
    print("="*50)
    print(f"\nActivate: {act}")
    print("Run simulation: python keylogger.py --max-keys 50")
    print("Analyze logs:  python detection.py --file sample_sysmon.xml\n")

def main():
    print("KEYLOGGER DETECTION PROJECT - SETUP\n" + "="*50)
    if not check_python(): sys.exit(1)
    venv = create_venv()
    if not venv: sys.exit(1)
    install_deps(venv)
    make_dirs()
    usage(venv)

if __name__ == "__main__":
    main()
