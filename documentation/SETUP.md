# Hydra-TouchDesigner Setup Guide

Step-by-step instructions for setting up the Hydra-TouchDesigner integration system.

## Prerequisites

### Software Requirements

- **TouchDesigner** 2023.11xxx or newer
  - Download from: https://derivative.ca/download
  - Commercial or Educational license

- **Python** 3.9+ (included with TouchDesigner)
  - TD uses its own embedded Python

- **Internet Connection**
  - Required for Hydra CDN (https://unpkg.com/hydra-synth)

### Hardware Requirements

- **Minimum:**
  - CPU: Quad-core processor
  - RAM: 8GB
  - GPU: DirectX 11 compatible
  - Display: 1920x1080

- **Recommended:**
  - CPU: 8+ cores
  - RAM: 16GB+
  - GPU: NVIDIA/AMD with 4GB+ VRAM
  - Display: 2560x1440 or higher

### Optional Hardware

- **Webcam** - For video input features
- **Microphone** - For audio reactivity
- **MIDI Controller** - For parameter control
- **AxiDraw Plotter** - For pen plotting output

## Installation

### Step 1: Install Python Dependencies

TouchDesigner uses its own Python environment. Install dependencies using TD's Python:

**On Windows:**
```bash
# Navigate to TouchDesigner's Python directory
cd "C:\Program Files\Derivative\TouchDesigner\bin\python"

# Install required packages
.\python.exe -m pip install opencv-python numpy requests
```

**On macOS:**
```bash
# Navigate to TouchDesigner's Python directory
cd "/Applications/TouchDesigner.app/Contents/Frameworks/Python.framework/Versions/Current/bin"

# Install required packages
./python3 -m pip install opencv-python numpy requests
```

**Alternative Method (within TouchDesigner):**

1. Open TouchDesigner
2. Open Textport (Alt+T or Cmd+T)
3. Run:
```python
import subprocess
import sys

# Install packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "numpy", "requests"])
```

### Step 2: Optional WebRTC Dependencies

For full video streaming capabilities (Phase 2):

```bash
./python -m pip install aiohttp aiortc
```

**Note:** WebRTC is optional. Basic webcam functionality works without it.

### Step 3: Project Setup

#### Method A: Using This Repository

1. Clone or download this repository
2. Open TouchDesigner
3. Create new project: `File > New`
4. Save as: `HydraTD.toe` in the repository folder
5. Follow the component creation steps below

#### Method B: Starting from Scratch

1. Create project folder structure:
```
HydraTD/
├── components/
├── scripts/
├── html/
├── presets/
│   └── examples/
├── exports/
└── docs/
```

2. Copy all files from this repository into appropriate folders

## Building the System

### Phase 1: Core Components (Required)

Follow these steps to build the core system:

#### 1. Create Base Structure

In TouchDesigner, create the following network structure:

```
/project1
├── /hydra_system (Base COMP)
│   ├── /core (Base COMP)
│   ├── /data (Base COMP)
│   ├── /code (Base COMP)
│   └── /output (Base COMP)
└── /QuickStart (Base COMP)
```

**How to create:**
- Press `Tab` in Network Editor
- Type "base" and select "Base COMP"
- Name according to structure above
- Nest components by dragging into parent

#### 2. Build HydraCore

Inside `/hydra_system/core`:

1. Create Base COMP named `HydraCore`
2. Inside HydraCore, create:
   - Text DAT named `hydra_html`
   - Copy contents from `/html/hydra_template.html`
3. Create Web Render TOP named `hydra_render`
   - Resolution: 1280x1280
   - HTML Source: Custom HTML
   - Custom HTML DAT: `hydra_html`
   - Enable "Cook Every Frame"

#### 3. Build DataBridge

Inside `/hydra_system/data`:

1. Create Base COMP named `DataBridge`
2. Inside DataBridge, create:
   - Table DAT named `chop_registry`
   - Add columns: `chop_path`, `enabled`, `update_rate`
   - Add header row
3. Create Text DAT named `data_collector`
   - Copy contents from `/scripts/data_bridge.py`
4. Create CHOP Execute DAT named `update_trigger`
   - CHOP parameter: `/project1/lfo1` (will create later)
   - Code:
```python
def onFrameEnd(channel, sampleIndex, val, prev):
    if me.time.frame % 2 == 0:  # 30fps throttle
        parent().op('data_collector').module.sendToHydra()
```

#### 4. Build CodeManager

Inside `/hydra_system/code`:

1. Create Base COMP named `CodeManager`
2. Inside CodeManager, create:
   - 3x Text DAT: `scene1_code`, `scene2_code`, `scene3_code`
   - Table DAT named `scene_registry`
     - Columns: `scene_name`, `dat_name`, `active`
     - Rows: See example below
   - Constant CHOP named `apply_mode`
     - Add channel: `auto` = 1
   - Text DAT named `code_executor`
     - Copy contents from `/scripts/code_manager.py`

**Scene Registry Example:**
```
scene_name | dat_name     | active
Scene 1    | scene1_code  | 1
Scene 2    | scene2_code  | 0
Scene 3    | scene3_code  | 0
```

#### 5. Build QuickStart

In `/project1`:

1. Create Base COMP named `QuickStart`
2. Inside QuickStart, create:
   - Text DAT named `init_script`
   - Copy contents from `/scripts/quickstart.py`
3. Create Button COMP named `setup_button`
   - Label: "Initialize Hydra System"
   - Script: `op('init_script').module.initialize()`

### Phase 2: Advanced Components (Optional)

#### 6. Build OutputRouter

Inside `/hydra_system/output`:

1. Create Base COMP named `OutputRouter`
2. Inside, create:
   - 4x Web Render TOP: `output_o0`, `output_o1`, `output_o2`, `output_o3`
   - Same HTML as HydraCore
   - Constant CHOP `output_enable` with 4 channels: `o0`, `o1`, `o2`, `o3`

#### 7. Build StateManager

Inside `/hydra_system`:

1. Create Base COMP named `StateManager`
2. Inside, create:
   - Text DAT named `preset_manager`
   - Copy contents from `/scripts/state_manager.py`

#### 8. Build SVGExporter

Inside `/hydra_system`:

1. Create Base COMP named `SVGExporter`
2. Inside, create:
   - Text DAT named `svg_converter`
   - Copy contents from `/scripts/svg_exporter.py`
   - Constant CHOP named `thresholds`
     - Channels: `threshold1` = 50, `threshold2` = 150

#### 9. Build ParameterInterface

Inside `/hydra_system`:

1. Create Base COMP named `ParameterInterface`
2. Inside, create:
   - Table DAT named `param_definitions`
   - Columns: `name`, `min`, `max`, `default`, `value`
   - Table CHOP named `params_to_chop`
     - Input: `param_definitions`
     - Select column: `value`

## First Run

### Initialize the System

1. Navigate to `/project1/QuickStart`
2. Click the `setup_button`
3. Wait for initialization to complete
4. Check TextPort (Alt+T) for confirmation messages

You should see:
```
HYDRA-TOUCHDESIGNER QUICKSTART INITIALIZATION
Step 1: Creating LFO CHOPs...
...
✓ HYDRA-TOUCHDESIGNER SYSTEM READY!
```

### Verify Installation

Run system diagnostic:
```python
op('/project1/QuickStart/init_script').module.checkSystem()
```

Expected output:
```
SYSTEM DIAGNOSTIC CHECK
  ✓ HydraCore: Found
  ✓ DataBridge: Found
  ✓ CodeManager: Found
  ...
✓ ALL SYSTEMS OPERATIONAL
```

### Test Basic Functionality

1. **Check Hydra Rendering:**
   - Navigate to `/hydra_system/core/HydraCore`
   - You should see animated oscillator pattern in `hydra_render` TOP

2. **Test CHOP Integration:**
   - Open Web Inspector on `hydra_render` (right-click > Inspect)
   - In console, type: `window.tdData`
   - Should show LFO values updating

3. **Edit Code:**
   - Navigate to `/hydra_system/code/CodeManager`
   - Edit `scene1_code` Text DAT
   - Change code to:
```javascript
osc(20, 0.1, 1)
  .color(1, 0, 0)
  .out()
```
   - Save and watch Hydra output update

## Troubleshooting Installation

### Web Render TOP shows black screen

**Cause:** HTML template not loaded or no internet

**Fix:**
1. Check `hydra_html` Text DAT has content
2. Verify internet connection (Hydra CDN)
3. Check Web Inspector for JavaScript errors
4. Try refreshing Web Render TOP (right-click > Reload)

### Python module import errors

**Cause:** Dependencies not installed in TD's Python

**Fix:**
```python
# In TextPort
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "opencv-python", "numpy", "requests"])
```

### QuickStart fails

**Cause:** Missing components or incorrect paths

**Fix:**
1. Verify all components exist at correct paths
2. Check TextPort for specific error messages
3. Manually create missing components
4. Try `checkSystem()` to identify issues

### CHOPs not found error

**Cause:** LFOs not created yet

**Fix:**
- Run QuickStart initialization
- Or manually create LFOs in `/project1`

### Performance issues

**Cause:** System overload

**Fix:**
1. Lower CHOP update rate to 30Hz or 15Hz
2. Reduce Web Render TOP resolution
3. Disable cook on unused TOPs
4. Simplify Hydra code

## Next Steps

After successful installation:

1. **Read Documentation:**
   - [README.md](README.md) - Feature overview
   - [API.md](API.md) - Complete API reference

2. **Try Examples:**
   - Edit example scenes in CodeManager
   - Load example presets from `/presets/examples`

3. **Customize:**
   - Add your own CHOPs to DataBridge
   - Create new scenes
   - Build custom parameters

4. **Experiment:**
   - Try audio reactivity
   - Test webcam input
   - Export to SVG

## AxiDraw Setup (Optional)

For pen plotting functionality:

1. **Install AxiDraw Software:**
   - Download from: https://axidraw.com/doc/cli_api/

2. **Install Python AxiDraw:**
```bash
pip install pyaxidraw
```

3. **Start AxiDraw Server:**
   - Create a simple Flask server or use provided script
   - Run on `localhost:8000`

4. **Test Connection:**
```python
op('svg_converter').module.captureAndPlot()
```

## Getting Help

- **Check Console:** TextPort (Alt+T) shows all error messages
- **Web Inspector:** Right-click Web Render TOP > Inspect for JavaScript errors
- **System Check:** Run `checkSystem()` for diagnostics
- **Hydra Docs:** https://hydra.ojack.xyz/
- **TD Docs:** https://docs.derivative.ca/

## Backup and Version Control

**Save regularly:**
- `File > Save` or Ctrl+S
- Create `.toe` backups before major changes

**Export components:**
- Right-click component > Save As > Component (.tox)
- Store in `/components` folder

**Presets:**
- Save your configurations as presets
- Back up `/presets` folder

---

**Setup Complete!** You're ready to start live coding with Hydra in TouchDesigner.

Next: Read [README.md](README.md) for usage instructions.
