# Hydra-TouchDesigner API Reference

Complete reference for all available functions in the Hydra-TouchDesigner integration.

## Table of Contents

- [JavaScript API (In Hydra Code)](#javascript-api-in-hydra-code)
- [Python API (TouchDesigner Scripts)](#python-api-touchdesigner-scripts)
- [Data Structures](#data-structures)

---

## JavaScript API (In Hydra Code)

These functions are available within your Hydra code in scene DATs.

### CHOP Access Functions

#### `chop(name, index)`

Access TouchDesigner CHOP channel by name and index.

**Parameters:**
- `name` (string): Name of the CHOP operator
- `index` (number): Channel index (0-based)

**Returns:** Function that evaluates to current channel value

**Example:**
```javascript
osc(chop('lfo1', 0) * 20, 0.1, chop('lfo2', 0)).out()
```

#### `lfo(index)`

Shorthand for accessing LFO CHOPs.

**Parameters:**
- `index` (number): LFO number (1-4)

**Returns:** Function returning LFO value

**Example:**
```javascript
osc(lfo(1) * 20, 0.1, lfo(2)).out()
```

#### `midi(cc)`

Access MIDI CC value.

**Parameters:**
- `cc` (number): MIDI CC number

**Returns:** Function returning MIDI value (0-1)

**Example:**
```javascript
osc(10, 0.1, midi(1)).out()
```

#### `audioFFT(index)`

Access TouchDesigner audio analysis FFT band.

**Parameters:**
- `index` (number): FFT band index

**Returns:** Function returning FFT value

**Example:**
```javascript
osc(10, 0.1, audioFFT(0) * 5).out()
```

### Hydra Built-in Audio

#### `a.fft[index]`

Hydra's built-in audio FFT (from microphone).

**Parameters:**
- `index` (number): FFT band index

**Returns:** Number (0-1)

**Example:**
```javascript
osc(10, 0.1, () => a.fft[0]).out()
```

### Video Sources

#### `s0.initCam()`

Initialize webcam as video source.

**Example:**
```javascript
s0.initCam()
src(s0).modulate(osc(10)).out()
```

#### `s0.initStream(url)`

Initialize WebRTC stream as video source.

**Parameters:**
- `url` (string): Stream URL

**Example:**
```javascript
s0.initStream('http://localhost:8080/stream')
src(s0).kaleid(4).out()
```

### Output Buffers

#### `.out(buffer)`

Render to specific output buffer.

**Parameters:**
- `buffer` (object): Output buffer (o0, o1, o2, or o3)

**Example:**
```javascript
osc(10).out(o0)
noise(3).out(o1)
shape(4).out(o2)
```

### Utility Functions

#### `clearAll()`

Clear all output buffers to black.

**Example:**
```javascript
clearAll()
```

---

## Python API (TouchDesigner Scripts)

### DataBridge Module

Location: `/scripts/data_bridge.py`

#### `collectCHOPData()`

Collect all enabled CHOPs from registry.

**Returns:** JSON string of CHOP data

**Example:**
```python
data = op('data_collector').module.collectCHOPData()
```

#### `sendToHydra()`

Send collected CHOP data to Hydra.

**Returns:** None

**Example:**
```python
op('data_collector').module.sendToHydra()
```

#### `addCHOPToRegistry(chop_path, enabled=True, update_rate=30)`

Add a new CHOP to the registry.

**Parameters:**
- `chop_path` (str): Full path to CHOP operator
- `enabled` (bool): Whether to enable data collection
- `update_rate` (int): Target update rate in Hz

**Returns:** bool (success status)

**Example:**
```python
op('data_bridge').module.addCHOPToRegistry('/project1/my_chop', enabled=True, update_rate=60)
```

#### `removeCHOPFromRegistry(chop_path)`

Remove a CHOP from the registry.

**Parameters:**
- `chop_path` (str): Full path to CHOP operator

**Returns:** bool (success status)

**Example:**
```python
op('data_bridge').module.removeCHOPFromRegistry('/project1/my_chop')
```

#### `toggleCHOP(chop_path)`

Toggle enabled state of a CHOP.

**Parameters:**
- `chop_path` (str): Full path to CHOP operator

**Returns:** bool (success status)

**Example:**
```python
op('data_bridge').module.toggleCHOP('/project1/lfo1')
```

#### `getActiveCHOPs()`

Get list of all active CHOPs.

**Returns:** List of CHOP paths

**Example:**
```python
active = op('data_bridge').module.getActiveCHOPs()
print(f"Active CHOPs: {active}")
```

#### `clearRegistry()`

Clear all CHOPs from registry (keeps header).

**Returns:** bool (success status)

**Example:**
```python
op('data_bridge').module.clearRegistry()
```

---

### CodeManager Module

Location: `/scripts/code_manager.py`

#### `executeCode(code)`

Send code string to Hydra for execution.

**Parameters:**
- `code` (str): JavaScript/Hydra code string

**Returns:** bool (success status)

**Example:**
```python
code = "osc(10, 0.1, 1).out()"
op('code_executor').module.executeCode(code)
```

#### `getActiveScene()`

Get currently active scene DAT.

**Returns:** DAT operator or None

**Example:**
```python
scene = op('code_executor').module.getActiveScene()
if scene:
    print(f"Active scene: {scene.name}")
```

#### `applyActiveScene()`

Execute code from the currently active scene.

**Returns:** bool (success status)

**Example:**
```python
op('code_executor').module.applyActiveScene()
```

#### `switchToScene(scene_name)`

Switch to a different scene by name.

**Parameters:**
- `scene_name` (str): Name of the scene (e.g., 'Scene 1')

**Returns:** bool (success status)

**Example:**
```python
op('code_executor').module.switchToScene('Scene 2')
```

#### `switchToSceneByIndex(index)`

Switch to scene by index (1-based).

**Parameters:**
- `index` (int): Scene number (1, 2, 3, etc.)

**Returns:** bool (success status)

**Example:**
```python
op('code_executor').module.switchToSceneByIndex(2)
```

#### `getSceneList()`

Get list of all available scenes.

**Returns:** List of scene names

**Example:**
```python
scenes = op('code_executor').module.getSceneList()
print(f"Available scenes: {scenes}")
```

#### `addScene(scene_name, dat_name)`

Add a new scene to the registry.

**Parameters:**
- `scene_name` (str): Display name for the scene
- `dat_name` (str): Name of the Text DAT containing code

**Returns:** bool (success status)

**Example:**
```python
op('code_executor').module.addScene('Scene 4', 'scene4_code')
```

#### `removeScene(scene_name)`

Remove a scene from the registry.

**Parameters:**
- `scene_name` (str): Name of the scene to remove

**Returns:** bool (success status)

**Example:**
```python
op('code_executor').module.removeScene('Scene 4')
```

#### `validateCode(code)`

Basic JavaScript syntax validation.

**Parameters:**
- `code` (str): JavaScript code string

**Returns:** Tuple (bool, str) - (is_valid, error_message)

**Example:**
```python
valid, msg = op('code_executor').module.validateCode("osc(10).out()")
if not valid:
    print(f"Error: {msg}")
```

#### `getApplyMode()`

Get current apply mode.

**Returns:** 'auto' or 'manual'

**Example:**
```python
mode = op('code_executor').module.getApplyMode()
print(f"Apply mode: {mode}")
```

#### `setApplyMode(mode)`

Set apply mode.

**Parameters:**
- `mode` (str): 'auto' or 'manual'

**Returns:** bool (success status)

**Example:**
```python
op('code_executor').module.setApplyMode('auto')
```

#### `toggleApplyMode()`

Toggle between auto and manual apply modes.

**Returns:** str (new mode)

**Example:**
```python
new_mode = op('code_executor').module.toggleApplyMode()
print(f"Switched to: {new_mode}")
```

---

### StateManager Module

Location: `/scripts/state_manager.py`

#### `savePreset(name)`

Save current state as a preset.

**Parameters:**
- `name` (str): Preset name (without .json extension)

**Returns:** bool (success status)

**Example:**
```python
op('preset_manager').module.savePreset('my_preset')
```

#### `loadPreset(name)`

Load a preset and apply state.

**Parameters:**
- `name` (str): Preset name (without .json extension)

**Returns:** bool (success status)

**Example:**
```python
op('preset_manager').module.loadPreset('my_preset')
```

#### `listPresets()`

Get list of available presets.

**Returns:** List of preset names

**Example:**
```python
presets = op('preset_manager').module.listPresets()
for p in presets:
    print(f"- {p}")
```

#### `deletePreset(name)`

Delete a preset.

**Parameters:**
- `name` (str): Preset name (without .json extension)

**Returns:** bool (success status)

**Example:**
```python
op('preset_manager').module.deletePreset('old_preset')
```

#### `getPresetInfo(name)`

Get information about a preset without loading it.

**Parameters:**
- `name` (str): Preset name (without .json extension)

**Returns:** dict (preset metadata) or None

**Example:**
```python
info = op('preset_manager').module.getPresetInfo('my_preset')
if info:
    print(f"Scenes: {info['scene_count']}, CHOPs: {info['chop_count']}")
```

---

### SVGExporter Module

Location: `/scripts/svg_exporter.py`

#### `captureFrame()`

Capture current Hydra output as numpy array.

**Returns:** numpy array (uint8) or None

**Example:**
```python
img = op('svg_converter').module.captureFrame()
```

#### `imageToSVG(img, threshold1=50, threshold2=150, simplify=True)`

Convert image to SVG using edge detection.

**Parameters:**
- `img` (ndarray): Image array
- `threshold1` (int): Lower threshold for Canny edge detection
- `threshold2` (int): Upper threshold for Canny edge detection
- `simplify` (bool): Apply polygon simplification

**Returns:** SVG string or None

**Example:**
```python
svg = op('svg_converter').module.imageToSVG(img, 100, 200, True)
```

#### `captureAndConvert(threshold1=50, threshold2=150, simplify=True)`

Capture and convert in one step.

**Parameters:**
- `threshold1` (int): Lower threshold
- `threshold2` (int): Upper threshold
- `simplify` (bool): Apply simplification

**Returns:** SVG string or None

**Example:**
```python
svg = op('svg_converter').module.captureAndConvert(75, 150)
```

#### `saveToFile(svg, filename=None)`

Save SVG to file.

**Parameters:**
- `svg` (str): SVG string
- `filename` (str): Optional filename (default: timestamped)

**Returns:** Path to saved file or None

**Example:**
```python
path = op('svg_converter').module.saveToFile(svg, 'my_art.svg')
```

#### `sendToAxiDraw(svg, server_url='http://localhost:8000/plot')`

Send SVG to AxiDraw server.

**Parameters:**
- `svg` (str): SVG string
- `server_url` (str): URL of AxiDraw server

**Returns:** bool (success status)

**Example:**
```python
success = op('svg_converter').module.sendToAxiDraw(svg)
```

#### `captureAndPlot(threshold1=50, threshold2=150, simplify=True, save_file=True)`

Complete workflow: capture, convert, save, and plot.

**Parameters:**
- `threshold1` (int): Lower threshold
- `threshold2` (int): Upper threshold
- `simplify` (bool): Apply simplification
- `save_file` (bool): Whether to save file locally

**Returns:** bool (success status)

**Example:**
```python
op('svg_converter').module.captureAndPlot(100, 200, True, True)
```

#### `getEdgePreview(threshold1=50, threshold2=150)`

Generate edge detection preview for threshold adjustment.

**Parameters:**
- `threshold1` (int): Lower threshold
- `threshold2` (int): Upper threshold

**Returns:** numpy array of edges or None

**Example:**
```python
preview = op('svg_converter').module.getEdgePreview(50, 150)
```

---

### QuickStart Module

Location: `/scripts/quickstart.py`

#### `initialize()`

Complete system initialization with default configuration.

**Returns:** bool (success status)

**Example:**
```python
op('init_script').module.initialize()
```

#### `checkSystem()`

Check if all system components are present and properly configured.

**Returns:** bool (all components OK)

**Example:**
```python
op('init_script').module.checkSystem()
```

#### `reset()`

Reset system to initial QuickStart state.

**Returns:** bool (success status)

**Example:**
```python
op('init_script').module.reset()
```

---

## Data Structures

### CHOP Registry Table

**Columns:**
- `chop_path` (str): Full path to CHOP operator
- `enabled` (str): '1' for enabled, '0' for disabled
- `update_rate` (str): Target update rate in Hz

**Example:**
```
chop_path              | enabled | update_rate
/project1/lfo1         | 1       | 30
/project1/audioanalysis| 1       | 60
```

### Scene Registry Table

**Columns:**
- `scene_name` (str): Display name
- `dat_name` (str): Text DAT containing code
- `active` (str): '1' for active, '0' for inactive

**Example:**
```
scene_name | dat_name     | active
Scene 1    | scene1_code  | 1
Scene 2    | scene2_code  | 0
```

### Parameter Definitions Table

**Columns:**
- `name` (str): Parameter name
- `min` (str): Minimum value
- `max` (str): Maximum value
- `default` (str): Default value
- `value` (str): Current value

**Example:**
```
name       | min | max | default | value
frequency  | 0   | 100 | 10      | 25.5
speed      | 0   | 2   | 1       | 1.2
```

### Preset JSON Structure

```json
{
  "version": "1.0",
  "name": "preset_name",
  "timestamp": "2025-10-09T12:00:00",
  "scenes": {
    "Scene 1": {
      "code": "osc(10).out()",
      "active": true
    }
  },
  "chop_mappings": [
    {
      "path": "/project1/lfo1",
      "enabled": true,
      "update_rate": 30
    }
  ],
  "parameters": {
    "frequency": 10.0,
    "speed": 1.0
  },
  "active_outputs": [0, 1],
  "apply_mode": "auto"
}
```

### TD Data Object (JavaScript)

Available as `window.tdData` in Hydra:

```javascript
{
  chops: {
    'lfo1': [0.5],
    'lfo2': [0.3],
    'audio_spectrum': [0.1, 0.2, 0.3, 0.4]
  },
  timestamp: 1696867200000,
  updateCount: 1234
}
```

### Performance Object (JavaScript)

Available as `window.tdPerformance` in Hydra:

```javascript
{
  fps: 59.8,
  frameTime: 16.7,
  lastUpdate: 1696867200000,
  chopUpdateRate: 30.0
}
```

---

## Error Handling

All Python functions include try-catch blocks and print diagnostic messages to the TouchDesigner console. Check the console for detailed error information.

Common error patterns:

```python
# Check if component exists
component = op('/path/to/component')
if not component:
    print("Error: Component not found")
    return False

# Validate return values
result = some_function()
if result is None:
    print("Function failed")
    return False
```

---

## Best Practices

1. **Always use absolute paths** for CHOP references
2. **Check function return values** before proceeding
3. **Use Web Inspector** for debugging JavaScript errors
4. **Save presets frequently** to preserve your work
5. **Monitor performance** and adjust update rates as needed

---

**Version**: 1.0
**Last Updated**: 2025-10-09
