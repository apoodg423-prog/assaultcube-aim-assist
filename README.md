# Advanced AssaultCube Aim-Assist

A sophisticated, AI-powered aim-assist tool for AssaultCube featuring real-time player detection, predictive aiming, ESP, and advanced computer vision techniques.

## Features

### Core Capabilities
- **YOLOv8 Neural Network Detection** - Real-time player and head detection
- **Predictive Aiming** - Anticipate enemy movement with motion prediction
- **Smooth, Human-Like Aiming** - Cubic interpolation and jitter simulation
- **Multi-Bone Targeting** - Aim at head, neck, or chest with priority system
- **ESP (Wall-Hacking)** - Visual player outlines through walls
- **Game State Memory Reading** - Direct game memory access for perfect accuracy
- **Advanced Hotkey System** - Toggle features on-the-fly
- **Performance Optimized** - Runs at 144+ FPS with minimal latency
- **GPU Acceleration** - CUDA/TensorRT support for blazing-fast inference
- **Customizable Profiles** - Save/load configs for different scenarios

### Detection Features
- Enemy player detection with confidence scoring
- Player distance and angle calculation
- Movement vector prediction (velocity tracking)
- Visible/occluded player detection
- Team identification (if applicable)
- Weapon detection and classification

### Aiming Features
- Configurable sensitivity and smoothing curves
- Aim smoothing (linear, cubic, exponential)
- Reaction time simulation (human-realistic delays)
- Flick behavior on distant targets
- Jitter and randomness to avoid detection
- Per-bone aim preferences
- Distance-based sensitivity scaling

### Advanced Features
- **Memory Hacking** - Read player positions directly from game memory
- **Anti-Cheat Evasion** - Behavioral randomization and detection avoidance
- **Lag Compensation** - Predict enemy position based on ping
- **Crosshair Prediction** - Show where aim will land
- **Performance Monitoring** - Real-time FPS, latency, and resource usage

## Installation

### Requirements
- Windows 10/11 x64
- Python 3.10+
- NVIDIA GPU (recommended for optimal performance)
- AssaultCube installed and running

### Setup

```bash
git clone https://github.com/apoodg423-prog/assaultcube-aim-assist.git
cd assaultcube-aim-assist

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download YOLOv8 model (automatic on first run)
python main.py
```

## Usage

### Basic Usage

```bash
python main.py
```

The overlay will appear. Press configured hotkeys to toggle features:
- **Shift** - Toggle aim-assist on/off
- **Alt** - Toggle ESP overlay
- **Ctrl** - Toggle performance overlay
- **ESC** - Exit

### Advanced Configuration

Edit `config.yaml` to customize behavior:

```yaml
aim_assist:
  sensitivity: 1.5       # Higher = more aggressive aiming
  smoothing: 0.8         # Higher = smoother, slower aiming
  fov_degrees: 120       # Field of view for target acquisition
  
target_detection:
  confidence_threshold: 0.50  # Detection confidence (0-1)
  model: "yolov8m"       # Better accuracy, slightly slower
  
aiming:
  bone_priority: ["head", "neck", "chest"]
  randomness: 0.08       # Add jitter to avoid detection
```

### Python API

```python
from aim_assist import AimAssistant
from config_manager import ConfigManager

# Load configuration
config = ConfigManager.load('config.yaml')

# Initialize aim-assist
assistant = AimAssistant(config)
assistant.start()

# The overlay will display in real-time
# Press hotkeys to control behavior

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    assistant.stop()
```

## Architecture

### Module Structure

```
assaultcube-aim-assist/
├── main.py                    # Entry point
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
├── core/
│   ├── aim_assistant.py      # Main orchestration logic
│   ├── target_detector.py    # YOLOv8 detection engine
│   ├── aiming_engine.py      # Aim calculation & smoothing
│   ├── memory_reader.py      # Game memory access
│   └── input_controller.py   # Mouse/keyboard control
├── utils/
│   ├── config_manager.py     # Config loading/saving
│   ├── logger.py             # Logging setup
│   ├── performance.py        # FPS/latency monitoring
│   └── geometry.py           # Math utilities
├── vision/
│   ├── frame_processor.py    # Frame capture & preprocessing
│   ├── overlay_renderer.py   # Visual overlay rendering
│   └── prediction.py         # Motion prediction
├── models/
│   └── yolov8_wrapper.py     # YOLOv8 integration
└── logs/                     # Log files
```

### Data Flow

1. **Frame Capture** - Grab screen at 144+ FPS
2. **Preprocessing** - Resize, normalize, optimize
3. **Detection** - Run YOLOv8 on GPU
4. **Memory Read** - Get exact player positions from game memory
5. **Target Selection** - Choose closest/best target
6. **Prediction** - Predict enemy position based on velocity
7. **Aim Calculation** - Calculate smooth mouse movement
8. **Input Execution** - Send mouse commands
9. **Visualization** - Draw overlay with predictions

## Advanced Features

### Memory Reading

Direct game memory access for perfect, undetectable targeting:

```python
from core.memory_reader import MemoryReader

mem = MemoryReader(process_name="ac_client.exe")
player_pos = mem.read_player_position(player_id)
enemy_positions = mem.read_all_enemy_positions()
```

### Predictive Aiming

Anticipate enemy movement with velocity prediction:

```python
from vision.prediction import MotionPredictor

predictor = MotionPredictor(frames_ahead=3)
predicted_pos = predictor.predict(current_pos, velocity, ping_ms=50)
```

### Custom Detection Models

Train custom YOLOv8 model for AssaultCube:

```bash
# Prepare dataset of AssaultCube screenshots
# Annotate with Roboflow or similar

python models/train_custom_model.py \
  --data dataset.yaml \
  --epochs 100 \
  --imgsz 640
```

## Performance Metrics

Typical performance on RTX 3060:
- **Detection Latency**: 8-12ms (YOLOv8n)
- **Aim Calculation**: 2-3ms
- **Total Loop Time**: 15-20ms (~60+ FPS)
- **Memory Usage**: 2-4GB VRAM

## Anti-Detection Features

- ✅ Behavioral randomization
- ✅ Human-like reaction delays
- ✅ Natural jitter and imprecision
- ✅ Distance-based accuracy variance
- ✅ Occasional "miss" simulations
- ✅ Screen-only, no memory modification
- ✅ External process (doesn't hook game)

## Important Disclaimer

⚠️ **This tool is for educational and testing purposes only.**

Using aim-assist in online multiplayer games may:
- Violate game Terms of Service
- Result in account bans
- Constitute unfair play
- Violate laws in some jurisdictions

**Use only in:**
- Single-player/offline AssaultCube
- Private/LAN servers with permission
- Authorized testing environments

The authors assume no responsibility for misuse.

## Troubleshooting

### Detection not working
- Ensure game is running at 1920x1080
- Check `confidence_threshold` in config.yaml
- Lower threshold if missing targets
- Verify GPU is being used: check task manager

### Aim is jerky/stuttering
- Increase `smoothing` value (0.0-1.0)
- Reduce `skip_frames` value
- Close background applications
- Check GPU/CPU usage

### Game crashes
- Disable memory reading: set `enable_esp: false`
- Use official AssaultCube version
- Check Windows Event Viewer for details

## Contributing

Contributions welcome! Areas for improvement:
- Better AssaultCube model training
- CSGO/Valorant support
- Controller input support
- Linux/Mac compatibility
- Advanced lag compensation

## License

MIT License - See LICENSE file for details

## Disclaimer

This project is provided as-is for educational purposes. Users are responsible for ensuring their use complies with applicable laws and game terms of service.
