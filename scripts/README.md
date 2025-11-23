# 📜 Scripts Directory

This directory contains automation scripts for building, installing, and releasing Get_transform.

## 📁 Scripts Overview

| Script | Platform | Purpose |
|--------|----------|---------|
| `build_executable.py` | All | Main build automation script (Python) |
| `build.sh` | Linux/macOS | Shell build script with colored output |
| `build.ps1` | Windows | PowerShell build script |
| `install.sh` | Linux/macOS | Installation script (creates venv) |
| `install.ps1` | Windows | Installation script (creates venv) |
| `prepare_release.sh` | Linux/macOS | Release preparation automation |

---

## 🔨 Build Scripts

### build_executable.py

**Main Python build script** - Works on all platforms

```bash
# Show help
python scripts/build_executable.py --help

# Basic build
python scripts/build_executable.py

# Auto-install PyInstaller and build
python scripts/build_executable.py --install-pyinstaller

# Clean build
python scripts/build_executable.py --clean

# Debug build
python scripts/build_executable.py --debug

# Build and test
python scripts/build_executable.py --test

# Full workflow
python scripts/build_executable.py --clean --install-pyinstaller --test
```

**Features**:
- ✅ Auto-checks for PyInstaller
- ✅ Interactive installation prompt
- ✅ Detailed progress reporting
- ✅ Error handling with solutions
- ✅ Post-build information display

---

### build.sh

**Linux/macOS shell script** - Bash-based build automation

```bash
# Show help
./scripts/build.sh --help

# Basic build
./scripts/build.sh

# Install dependencies and build
./scripts/build.sh --install-deps

# Clean build
./scripts/build.sh --clean

# Build with test
./scripts/build.sh --test

# Debug build
./scripts/build.sh --debug
```

**Features**:
- ✅ Colorized terminal output
- ✅ Error handling (set -e)
- ✅ Python version check
- ✅ File size reporting
- ✅ User-friendly messages

---

### build.ps1

**Windows PowerShell script** - Native Windows build automation

```powershell
# Show help
.\scripts\build.ps1 -Help

# Basic build
.\scripts\build.ps1

# Install dependencies and build
.\scripts\build.ps1 -InstallDeps

# Clean build
.\scripts\build.ps1 -Clean

# Build with test
.\scripts\build.ps1 -Test

# Debug build
.\scripts\build.ps1 -Debug
```

**Features**:
- ✅ PowerShell parameter syntax
- ✅ Colorized output
- ✅ Python version check
- ✅ File size reporting
- ✅ Windows-friendly error messages

---

## 📦 Installation Scripts

### install.sh

**Linux/macOS installation script** - Sets up development environment

```bash
# Run installation
./scripts/install.sh
```

**What it does**:
1. Checks Python version
2. Creates virtual environment (.venv)
3. Upgrades pip
4. Installs project dependencies
5. Creates `run.sh` launcher script

**Output**: 
- `.venv/` - Virtual environment
- `run.sh` - Launcher script

**Usage after installation**:
```bash
./run.sh  # Run the application
```

---

### install.ps1

**Windows PowerShell installation script** - Sets up development environment

```powershell
# Run installation
.\scripts\install.ps1
```

**What it does**:
1. Checks Python version
2. Creates virtual environment (.venv)
3. Upgrades pip
4. Installs project dependencies
5. Creates `run.bat` launcher script

**Output**:
- `.venv\` - Virtual environment
- `run.bat` - Launcher script

**Usage after installation**:
```batch
.\run.bat  # Run the application
# or double-click run.bat
```

---

## 🚀 Release Scripts

### prepare_release.sh

**Release preparation automation** - Streamlines the release process

```bash
# Run release preparation
./scripts/prepare_release.sh
```

**What it does**:
1. ✅ Checks Git working directory status
2. ✅ Prompts for new version number
3. ✅ Runs test suite
4. ✅ Builds executable (optional)
5. ✅ Creates release directory with:
   - Executable file (renamed with version)
   - SHA256 checksum
   - Documentation files (README, BUILD, QUICKSTART, CHANGELOG)
   - Release notes
6. ✅ Prompts to update CHANGELOG.md
7. ✅ Generates RELEASE_NOTES.md
8. ✅ Shows release checklist
9. ✅ Creates Git commit and tag (optional)
10. ✅ Pushes to remote (optional)

**Output**:
- `release-vX.Y.Z/` - Release package directory
  - `get_transform-vX.Y.Z-platform-arch` - Executable
  - `get_transform-vX.Y.Z-platform-arch.sha256` - Checksum
  - `README.md`, `BUILD.md`, `QUICKSTART.md`, `CHANGELOG.md`
  - `RELEASE_NOTES.md` - Release announcement

---

## 🎯 Quick Start

### For Developers

**First time setup**:
```bash
# Linux/macOS
./scripts/install.sh
./run.sh

# Windows
.\scripts\install.ps1
.\run.bat
```

**Build executable**:
```bash
# Linux/macOS
./scripts/build.sh --install-deps

# Windows
.\scripts\build.ps1 -InstallDeps
```

---

### For Maintainers

**Prepare a release**:
```bash
# Run release automation (Linux/macOS)
./scripts/prepare_release.sh

# Then build on other platforms:
# - Windows: .\scripts\build.ps1 -InstallDeps
# - macOS: ./scripts/build.sh --install-deps

# Upload all platform executables to GitHub Release
```

---

## 📋 Platform Requirements

### All Platforms
- Python 3.6+
- pip (latest)
- 500MB disk space

### Windows
- PowerShell 5.1+
- Windows 10 or later

### macOS
- Bash shell
- Xcode Command Line Tools: `xcode-select --install`
- macOS 10.15+

### Linux
- Bash shell
- build-essential (gcc, make)
  ```bash
  # Ubuntu/Debian
  sudo apt-get install build-essential
  ```

---

## 🔍 Troubleshooting

### PyInstaller Not Found

**Problem**: `ModuleNotFoundError: No module named 'PyInstaller'`

**Solution**:
```bash
# Install PyInstaller
pip install pyinstaller

# Or use the --install-pyinstaller flag
python scripts/build_executable.py --install-pyinstaller
```

---

### Permission Denied (Linux/macOS)

**Problem**: `bash: ./scripts/build.sh: Permission denied`

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/*.sh scripts/*.py
```

---

### Build Fails with Missing Module

**Problem**: `ImportError: cannot import name 'xyz'`

**Solution**:
1. Check `get_transform.spec` - add to `hiddenimports`
2. Or install missing package: `pip install package-name`

---

### Windows Execution Policy Error

**Problem**: `cannot be loaded because running scripts is disabled`

**Solution**:
```powershell
# Allow script execution (run PowerShell as Administrator)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass
powershell -ExecutionPolicy Bypass -File .\scripts\build.ps1
```

---

## 📚 Related Documentation

- [BUILD.md](../BUILD.md) - Comprehensive build documentation
- [QUICKSTART.md](../QUICKSTART.md) - User quick start guide
- [PACKAGING.md](../PACKAGING.md) - Packaging technical details
- [README.md](../README.md) - Project overview

---

## 🤝 Contributing

When adding new scripts:
1. Add shebang line (`#!/usr/bin/env python3` or `#!/bin/bash`)
2. Make executable: `chmod +x script_name`
3. Add usage documentation to this README
4. Test on target platform(s)
5. Handle errors gracefully
6. Provide helpful error messages

---

**Maintained by**: Get_transform Team  
**Last Updated**: 2025-01-27
