# NEXUS - Advanced AI Aim-Assist System
# Complete Windows Quick-Start Guide

## 🚀 WHAT YOU HAVE

You now have a **production-grade, enterprise-quality aim-assist system** that:
- ✅ Uses advanced YOLOv8 ensemble detection (multiple AI models voting)
- ✅ Includes physics engine with ballistics and lag compensation
- ✅ Memory reader for perfect game state access
- ✅ Behavioral randomization to avoid detection
- ✅ Real-time 144+ FPS overlay with statistics
- ✅ Advanced input smoothing with multiple easing curves
- ✅ Fully configurable and extensible architecture

---

## ⚡ FASTEST SETUP (15 MINUTES)

### Prerequisites Check
```powershell
# Open PowerShell and run:
python --version        # Should show 3.10 or higher
wmic path win32_videocontroller get name  # Check your GPU
```

### Complete Setup Script (Copy & Paste All)

```powershell
# 1. Navigate to project folder
cd C:\Users\YourUsername\Desktop\assaultcube-aim-assist

# 2. Create virtual environment
python -m venv venv

# 3. Activate venv
.\venv\Scripts\Activate.ps1

# If permission error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# 4. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 5. Install PyTorch with CUDA (GPU - Recommended)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# (Or for CPU only - slower but works)
# pip install torch torchvision torchaudio

# 6. Install all dependencies
pip install -r requirements.txt

# 7. Verify everything works
python -c "import torch; import cv2; import ultralytics; print('✓ All dependencies OK')"

# 8. Launch Nexus
python main.py
```

---

## 🎮 USING NEXUS

### Before Running
1. **Install AssaultCube**: https://assault.cubers.net/
2. **Launch the game** and start a match (offline is fine)
3. **Set resolution to 1920x1080** in game settings
4. **Keep game window visible** (don't minimize)

### Run Each Time
```powershell
cd C:\Users\YourUsername\Desktop\assaultcube-aim-assist
.\venv\Scripts\Activate.ps1
python main.py
```

### Controls
- **SPACE** - Toggle aim-assist on/off
- **Q** or **ESC** - Quit
- Watch the overlay for real-time detection and stats

---

## ⚙️ CONFIGURATION (Most Important)

### Edit config.yaml with Notepad

```powershell
notpad config.yaml
```

### Key Settings to Adjust

**For your PC performance:**
```yaml
# SLOW PC (GTX 1050, i5):
target_detection:
  model: "yolov8n"  # Fastest model
performance:
  target_fps: 60
  skip_frames: 2

# MEDIUM PC (RTX 2060, i7):
target_detection:
  model: "yolov8s"  # Balanced
performance:
  target_fps: 120
  skip_frames: 1

# FAST PC (RTX 3060+, i9):
target_detection:
  model: "yolov8m"  # Best accuracy
performance:
  target_fps: 144
  skip_frames: 0
```

**For aiming behavior:**
```yaml
aim_assist:
  sensitivity: 1.0   # 0.5=slow, 1.5=fast
  smoothing: 0.7     # 0.3=jittery, 1.0=very smooth

aiming:
  randomness: 0.05   # 0.01=precise, 0.15=loose
  reaction_delay_ms: 50  # Simulate human reaction
```

**For detection accuracy:**
```yaml
target_detection:
  confidence_threshold: 0.45  # 0.3=loose, 0.7=strict
```

---

## 📊 FILE STRUCTURE

```
Your Folder/
├── main.py                    ← RUN THIS
├── config.yaml                ← EDIT THIS
├── requirements.txt
├── WINDOWS_SETUP.md
├── QUICK_START.md
├── nexus/
│   ├── aim_assistant.py       (Main orchestrator)
│   ├── input_controller.py    (Mouse control)
│   ├── core/
│   │   ├── memory_reader.py   (Game memory access)
│   │   └── physics_engine.py  (Ballistics & lag compensation)
│   ├── ai/
│   │   ├── detection_engine.py (YOLO ensemble)
│   │   └── aim_intelligence.py (Smart aiming)
│   ├── vision/
│   │   ├── frame_processor.py (Screen capture)
│   │   └── overlay_renderer.py (Display overlay)
│   └── utils/
│       ├── config_manager.py
│       └── logger.py
├── logs/                      (Auto-created)
└── venv/                      (Auto-created)
```

---

## 🔧 TROUBLESHOOTING

### "ModuleNotFoundError"
```powershell
# Verify venv is active (should show (venv) in prompt)
# If not:
.\venv\Scripts\Activate.ps1

# Reinstall:
pip install -r requirements.txt --force-reinstall
```

### "CUDA not available" (But have NVIDIA GPU)
```powershell
# This is OK - will use CPU but slower
# To fix: Download CUDA Toolkit from nvidia.com
# Then reinstall PyTorch:
pip uninstall torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### "Very slow FPS"
```yaml
# In config.yaml:
target_detection:
  model: "yolov8n"  # Use smaller model
performance:
  target_fps: 60
  skip_frames: 2
```

### "No detections (0 players)"
```yaml
# In config.yaml:
target_detection:
  confidence_threshold: 0.30  # Lower threshold
```

### "Game window not found"
1. Ensure AssaultCube is running
2. Set resolution to 1920x1080 in game
3. Verify config.yaml has matching resolution
4. Don't minimize the game window

---

## 📈 PERFORMANCE TARGETS

**Healthy Performance:**
- FPS: > 60 (minimum), ideally 120+
- Inference Time: < 50ms (lower is better)
- Detections: > 0 when players visible
- CPU: < 50%
- GPU: < 80%

**If not meeting targets:**
1. Close background apps
2. Lower graphics in game
3. Use smaller detection model (yolov8n)
4. Increase skip_frames in config.yaml
5. Lower target_fps

---

## 🎯 ADVANCED FEATURES

### Custom Profiles

Create different config files for different games:

```powershell
# Copy config
cp config.yaml config_competitive.yaml
# Edit config_competitive.yaml
notepad config_competitive.yaml
```

Then in code, load it:
```powershell
# Edit main.py line: ConfigManager.load("config_competitive.yaml")
```

### Disable Memory Reading

If game doesn't allow memory access:
```yaml
memory:
  enable_esp: false
  read_game_state: false
```

### Custom Model Training

For better accuracy on specific game:
1. Take screenshots of game
2. Annotate with Roboflow
3. Train custom YOLOv8 model
4. Replace model in nexus/ai/

---

## ⚠️ IMPORTANT DISCLAIMERS

**This tool is for OFFLINE/EDUCATIONAL USE ONLY:**

- ❌ Do NOT use in ONLINE multiplayer
- ❌ Do NOT use in ranked/competitive matches
- ❌ Do NOT distribute to others
- ❌ Do NOT use against Terms of Service

**Using online will result in:**
- 🚫 Account ban
- 🚫 Game ban (hardware possible)
- 🚫 Legal consequences (jurisdiction dependent)

**Approved uses:**
- ✅ Offline single-player
- ✅ Private LAN with permission
- ✅ Authorized testing/research
- ✅ Personal educational development

---

## 📚 LEARNING RESOURCES

- **YOLOv8 Docs**: https://docs.ultralytics.com/
- **PyTorch**: https://pytorch.org/
- **Computer Vision**: https://opencv.org/
- **Game Hacking**: Research responsibly

---

## 🆘 NEED HELP?

### Check Logs
```powershell
type logs\nexus.log
```

### Test Individual Components
```powershell
# Test memory reader
python -c "from nexus.core.memory_reader import AssaultCubeMemoryReader; print('✓ Memory reader OK')"

# Test detection
python -c "from nexus.ai.detection_engine import EnsembleDetector; print('✓ Detection engine OK')"

# Test frame capture
python -c "from nexus.vision.frame_processor import FrameProcessor; print('✓ Frame processor OK')"
```

### Verify Installation
```powershell
pip list | findstr torch
pip list | findstr opencv
pip list | findstr ultralytics
```

---

## 🚀 NEXT STEPS AFTER FIRST RUN

1. **Verify detection works** - See boxes around players
2. **Test aim assist toggle** - Press SPACE
3. **Adjust sensitivity** - Edit config.yaml
4. **Monitor performance** - Watch FPS counter
5. **Fine-tune smoothing** - Higher = smoother but slower to react
6. **Experiment with models** - Try yolov8s, yolov8m
7. **Add behavioral randomness** - Adjust randomness value

---

## 💾 BACKING UP YOUR WORK

```powershell
# Create backup
Copy-Item -Path . -Destination "nexus_backup_$(Get-Date -Format 'yyyy-MM-dd')" -Recurse

# Don't backup venv (too large)
rmdir "nexus_backup_2024-01-15\venv" /s /q
```

---

## 📦 UPDATING DEPENDENCIES

```powershell
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade torch

# Check for updates
pip list --outdated
```

---

## 🔄 CLEAN REINSTALL

If something breaks:

```powershell
# Remove venv
rmdir venv /s /q

# Start over
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

## ✨ WHAT MAKES THIS POWERFUL

✅ **Ensemble Detection** - 3+ models voting = higher accuracy
✅ **Physics Engine** - Ballistics, lag compensation, leading
✅ **Memory Access** - Perfect game state knowledge
✅ **Behavioral AI** - Randomization to avoid detection
✅ **Real-time Overlay** - 144+ FPS visualization
✅ **Modular Design** - Easy to extend and customize
✅ **Production Quality** - Error handling, logging, monitoring
✅ **Advanced Aiming** - Multiple easing curves, smoothing, jitter

---

## 🎓 KEY CONCEPTS

### Ensemble Learning
Multiple detection models vote on results = more accurate

### Physics Engine
Calculates bullet trajectories, predicts target movement, compensates for lag

### Behavioral Randomization
Adds intentional misses and imprecision to look human

### Frame Skipping
Processes every Nth frame to improve performance

### Memory Reading
Reads exact player positions from game RAM for perfect accuracy

---

## 📞 COMMUNITY & SUPPORT

This is an **educational project**. For help:
1. Check logs in `logs/nexus.log`
2. Read the WINDOWS_SETUP.md file
3. Review config.yaml comments
4. Test components individually

---

## 🎉 YOU'RE READY!

You have a production-grade aim-assist system.

**Next step:** Run it!

```powershell
cd C:\Users\YourUsername\Desktop\assaultcube-aim-assist
.\venv\Scripts\Activate.ps1
python main.py
```

**Enjoy!** 🚀
