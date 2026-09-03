# Nexus - Complete Step-by-Step Windows Setup Guide

## COMPLETE PROJECT FILE STRUCTURE

Your project should look like this after setup:

```
assaultcube-aim-assist/
├── main.py                          ← RUN THIS
├── config.yaml                      ← EDIT THIS
├── requirements.txt                 ← Install from this
├── INSTALL.md                       ← Installation guide
├── WINDOWS_SETUP.md                 ← This file
├── .gitignore
├── .env.example
│
├── nexus/
│   ├── __init__.py
│   ├── aim_assistant.py            ← Main orchestrator
│   ├── input_controller.py         ← Mouse/keyboard control
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── memory_reader.py        ← Game memory access
│   │   └── physics_engine.py       ← Ballistics & lag comp
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── detection_engine.py     ← YOLO ensemble
│   │   └── aim_intelligence.py     ← Smart aiming
│   │
│   ├── vision/
│   │   ├── __init__.py
│   │   ├── frame_processor.py      ← Screen capture
│   │   └── overlay_renderer.py     ← Visual overlay
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config_manager.py       ← Config loading
│       └── logger.py               ← Logging setup
│
└── logs/
    └── nexus.log                    ← Auto-created
```

---

## STEP 1: DOWNLOAD & VERIFY FILES

### Option A: Clone from GitHub (Recommended)

1. **Open PowerShell** (Windows key + type "PowerShell" + Enter)
2. **Navigate to Desktop or your desired location:**
   ```powershell
   cd $HOME\Desktop
   ```

3. **Clone the repository:**
   ```powershell
   git clone https://github.com/apoodg423-prog/assaultcube-aim-assist.git
   cd assaultcube-aim-assist
   ```

### Option B: Manual Download

1. Go to: https://github.com/apoodg423-prog/assaultcube-aim-assist
2. Click **"Code"** → **"Download ZIP"**
3. **Extract to Desktop or your folder**
4. **Open PowerShell in that folder** (File → Open PowerShell here)

### Verify All Files Are Present

```powershell
# Check if structure is correct
ls -R
```

You should see:
- `main.py` ✅
- `config.yaml` ✅
- `requirements.txt` ✅
- `nexus/` folder with subfolders ✅

If files are missing, download again or re-extract the ZIP.

---

## STEP 2: INSTALL PYTHON & VERIFY

### Check if Python is Installed

```powershell
python --version
```

**Expected output:** `Python 3.10.0` or higher

### If Python is NOT installed:

1. Download from: https://www.python.org/downloads/
2. Run the installer
3. **CRITICAL:** Check the box: **"Add Python to PATH"**
4. Click **"Install Now"**
5. After installation, **restart PowerShell**
6. Verify: `python --version`

---

## STEP 3: INSTALL NVIDIA CUDA & DRIVERS (For GPU Support)

### Check Your GPU

```powershell
# If you have NVIDIA GPU
wmic path win32_videocontroller get name
```

### Install NVIDIA Drivers

1. Go to: https://www.nvidia.com/Download/driverDetails.aspx
2. Select your GPU model and Windows version
3. Download and install
4. **Restart computer**

### Install CUDA Toolkit

1. Go to: https://developer.nvidia.com/cuda-downloads
2. Select:
   - **Operating System:** Windows
   - **Architecture:** x86_64
   - **Version:** 11 (or latest)
   - **Installer Type:** exe (network)
3. Download and run installer
4. Use default installation path
5. **Restart PowerShell after installation**

### Verify CUDA Installation

```powershell
nvcc --version
```

Should show CUDA version (e.g., "CUDA 11.8")

---

## STEP 4: CREATE VIRTUAL ENVIRONMENT

**In PowerShell (in your project folder):**

```powershell
# Navigate to project folder if not already there
cd C:\Users\YourUsername\Desktop\assaultcube-aim-assist

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

**If you get an error about execution policy:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Check activation successful:**

You should see `(venv)` at the beginning of the PowerShell line:
```
(venv) PS C:\Users\...\assaultcube-aim-assist>
```

---

## STEP 5: UPGRADE PIP & INSTALL DEPENDENCIES

**Make sure venv is activated (you see `(venv)` in prompt)**

```powershell
# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# This will take 2-3 minutes...
```

### Install PyTorch with CUDA Support (GPU)

```powershell
# For NVIDIA GPU (Recommended)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# This takes 5-10 minutes, be patient...
```

### Install All Other Dependencies

```powershell
# Install from requirements.txt
pip install -r requirements.txt

# This takes 10-15 minutes...
```

### Verify Installation

```powershell
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); import cv2; print(f'OpenCV: {cv2.__version__}')"
```

**Expected output:**
```
PyTorch: 2.0.0+cu118
CUDA Available: True
OpenCV: 4.8.0
```

If `CUDA Available: False`, continue anyway (will use CPU, slower)

---

## STEP 6: CONFIGURE config.yaml

### Open config.yaml

```powershell
# Open in Notepad
notpad config.yaml

# Or use any text editor (VS Code, Sublime, etc.)
```

### Default Configuration (for AssaultCube)

**Find these sections and verify/edit:**

```yaml
game:
  name: "AssaultCube"
  resolution:
    width: 1920        # Match your game resolution
    height: 1080       # Match your game resolution
  process_name: "ac_client.exe"

aim_assist:
  enabled: true
  sensitivity: 1.2        # 0.5 (slow) to 2.0 (fast)
  smoothing: 0.7          # 0.3 (jittery) to 1.0 (very smooth)
  fov_degrees: 120        # Field of view for detection

target_detection:
  model: "yolov8n"        # yolov8n (fast) or yolov8s (better)
  confidence_threshold: 0.45  # 0.3 (loose) to 0.7 (strict)
  enable_gpu: true        # Use GPU if available

aiming:
  bone_priority: ["head", "neck", "chest"]
  aim_smoothing_curve: "cubic"
  randomness: 0.05        # Add human-like jitter
  reaction_delay_ms: 50   # Reaction time simulation

hotkeys:
  toggle_aim: "shift"     # Hold Shift to activate aim
  exit: "esc"             # Press ESC to quit

performance:
  target_fps: 144
  skip_frames: 1
  use_multiprocessing: true

logging:
  level: "INFO"           # DEBUG, INFO, WARNING, ERROR
  log_file: "logs/aim_assist.log"
  console_output: true
```

### Quick Tuning Presets

**For Low-End PC (GTX 1050):**
```yaml
target_detection:
  model: "yolov8n"
  enable_gpu: true

performance:
  target_fps: 60
  skip_frames: 2
```

**For Mid-Range PC (RTX 2060):**
```yaml
target_detection:
  model: "yolov8s"
  enable_gpu: true

performance:
  target_fps: 120
  skip_frames: 1
```

**For High-End PC (RTX 3060+):**
```yaml
target_detection:
  model: "yolov8m"
  enable_gpu: true

performance:
  target_fps: 144
  skip_frames: 0
```

**Save the file** (Ctrl+S)

---

## STEP 7: PREPARE ASSAULTCUBE

1. **Download AssaultCube**: https://assault.cubers.net/
2. **Install and launch** the game
3. **Set resolution to 1920x1080**:
   - In-game settings → Graphics → Resolution
   - Match the resolution in `config.yaml`
4. **Start a game** (offline or local server)
5. **Keep the game window visible** (don't minimize)

---

## STEP 8: LAUNCH NEXUS

**In PowerShell (make sure you're in the project folder and venv is activated):**

```powershell
# Verify venv is active (should show (venv) in prompt)
# If not, run: .\venv\Scripts\Activate.ps1

# Launch Nexus
python main.py
```

**Expected output:**
```
[2024-01-15 10:30:45] [nexus.aim_assistant] [INFO] Starting Nexus Aim-Assist...
[2024-01-15 10:30:46] [nexus.core.memory_reader] [INFO] Connected to ac_client.exe
[2024-01-15 10:30:47] [nexus.ai.detection_engine] [INFO] Loading model: yolov8n
[2024-01-15 10:30:50] [nexus.aim_assistant] [INFO] Nexus started successfully
```

**Live display should open showing:**
- Game screen with detections
- Green boxes around players
- Red/yellow crosshair indicators
- FPS counter in top-left
- Detection statistics

---

## STEP 9: TEST & CONTROL

### While running:

**Hotkey Controls:**
- **SPACE** - Toggle aim-assist on/off
- **SHIFT** - (Alternative) Activate aim assist
- **Q** - Quit
- **ESC** - Exit (alternate)

### Check Performance

**In the overlay you'll see:**
- `FPS: 60` - Frames per second
- `Detections: 3` - Number of players detected
- `Inference Time: 15ms` - AI model speed
- `Aim Active: True/False` - Current state

**Target performance:**
- ✅ FPS > 60 (minimum)
- ✅ Inference time < 50ms
- ✅ Detections > 0 (when players visible)

---

## TROUBLESHOOTING

### Problem: "(venv) not showing in prompt"

**Solution:**
```powershell
.\venv\Scripts\Activate.ps1
```

If error about execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Problem: "ModuleNotFoundError: No module named 'torch'"

**Solution:**
```powershell
# Make sure venv is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Problem: "CUDA not available"

**Solution (will work but slower):**
```powershell
# Continue without CUDA - it will use CPU
# Performance will be slower but still works
# To fix:
# 1. Check if GPU detected: wmic path win32_videocontroller get name
# 2. Update NVIDIA drivers
# 3. Reinstall CUDA Toolkit
```

### Problem: "Game window not detected"

**Solution:**
1. Ensure AssaultCube is running
2. Set resolution to 1920x1080 in game
3. Verify in `config.yaml`:
   ```yaml
   game:
     resolution:
       width: 1920
       height: 1080
   ```
4. Don't minimize the game window

### Problem: "Very slow FPS (< 30)"

**Solution:**
```yaml
# In config.yaml, change to:
target_detection:
  model: "yolov8n"      # Use smaller model
  enable_gpu: true

performance:
  skip_frames: 2        # Process every 2nd frame
  target_fps: 60        # Lower target FPS
```

### Problem: "Detection boxes not showing"

**Solution:**
```yaml
# Lower confidence threshold in config.yaml:
target_detection:
  confidence_threshold: 0.30  # Was 0.45
```

### Problem: "No detections (0 players found)"

**Solution:**
1. Ensure players/enemies are visible in game
2. Try lowering confidence threshold
3. Check lighting in-game
4. Try different color settings in game

---

## COMPLETE COMMAND REFERENCE

**Full setup from scratch (copy-paste all these commands):**

```powershell
# 1. Navigate to project
cd C:\Users\YourUsername\Desktop\assaultcube-aim-assist

# 2. Create virtual environment
python -m venv venv

# 3. Activate venv
.\venv\Scripts\Activate.ps1

# 4. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 5. Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 6. Install dependencies
pip install -r requirements.txt

# 7. Verify installation
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); import cv2; print(f'OpenCV: {cv2.__version__}')"

# 8. Run Nexus
python main.py
```

---

## FILE CHECKLIST

Before running, verify you have these files:

- [ ] `main.py` - Main entry point
- [ ] `config.yaml` - Configuration file (EDIT THIS)
- [ ] `requirements.txt` - Python dependencies
- [ ] `INSTALL.md` - Installation guide
- [ ] `WINDOWS_SETUP.md` - This file
- [ ] `.gitignore` - Git ignore rules
- [ ] `.env.example` - Environment variables template

**Folders:**
- [ ] `nexus/` folder exists
- [ ] `nexus/__init__.py` exists
- [ ] `nexus/aim_assistant.py` exists
- [ ] `nexus/input_controller.py` exists
- [ ] `nexus/core/` folder with files
- [ ] `nexus/ai/` folder with files
- [ ] `nexus/vision/` folder with files
- [ ] `nexus/utils/` folder with files

**Auto-created on first run:**
- [ ] `venv/` folder (created by venv)
- [ ] `logs/` folder (created automatically)
- [ ] `logs/nexus.log` file (created automatically)

---

## WHAT HAPPENS ON FIRST RUN

When you run `python main.py` for the first time:

1. **Models download** (1-2 minutes)
   - YOLOv8 model downloaded (~200MB)
   - Saved to `~/.yolov8/` folder

2. **Game connection** (2-3 seconds)
   - Connects to AssaultCube game memory
   - Shows success message or warning

3. **Detection initialization** (5-10 seconds)
   - Models loaded to GPU/CPU
   - Performing test inference

4. **Display opens** (should show live feed)
   - Game screen visible
   - Detection overlays enabled
   - Real-time statistics showing

5. **Ready to use**
   - Press SPACE to toggle aim assist
   - Press Q to quit

---

## NEXT STEPS

After first successful run:

1. **Test in offline game** - Verify detections work
2. **Adjust sensitivity** - Edit `config.yaml` and re-run
3. **Monitor performance** - Watch FPS and inference time
4. **Customize behavior** - Tweak smoothing, randomness, etc.
5. **Add more models** - Improve accuracy with ensemble

---

## IMPORTANT DISCLAIMERS

⚠️ **WARNING:**

- This tool is for **OFFLINE/LOCAL TESTING ONLY**
- Using in **ONLINE multiplayer violates Terms of Service**
- May result in **ACCOUNT BAN**
- Authors assume **NO RESPONSIBILITY** for misuse
- Legal consequences possible in some jurisdictions

Use only in:
- ✅ Offline AssaultCube
- ✅ Private LAN servers with permission
- ✅ Authorized testing environments
- ✅ Educational/development purposes

---

## GETTING HELP

1. **Check logs:**
   ```powershell
   type logs\nexus.log
   ```

2. **Verify installation:**
   ```powershell
   pip list | findstr torch
   pip list | findstr opencv
   ```

3. **Test individual components:**
   ```powershell
   python -c "from nexus.core.memory_reader import AssaultCubeMemoryReader; print('Memory reader OK')"
   python -c "from nexus.ai.detection_engine import EnsembleDetector; print('Detection engine OK')"
   python -c "from nexus.vision.frame_processor import FrameProcessor; print('Frame processor OK')"
   ```

---

## Quick Reference

**Start fresh each time:**
```powershell
cd C:\Users\YourUsername\Desktop\assaultcube-aim-assist
.\venv\Scripts\Activate.ps1
python main.py
```

**Deactivate venv when done:**
```powershell
deactivate
```

**Update dependencies:**
```powershell
pip install --upgrade -r requirements.txt
```

**Clean reinstall:**
```powershell
rmdir venv /s /q
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

**Ready to go! Follow steps 1-9 and you'll be running Nexus in 30-60 minutes.** 🚀
