# Hydra-TouchDesigner Integration

A complete system for running the Hydra live coding environment inside TouchDesigner with full bidirectional data flow, enabling generative art and pen plotting workflows.

## Features

### Core System
- **Hydra Engine**: Full Hydra-Synth running in Web Render TOP
- **CHOP Integration**: Access any TouchDesigner CHOP via `chop('name', index)` function
- **Multi-Scene Management**: Switch between multiple Hydra code scenes
- **Video Streaming**: WebRTC support for external video sources
- **Audio Reactivity**: Dual audio input (Hydra built-in + TD analysis)
- **Multi-Output**: 4 independent output buffers (o0-o3)
- **Preset System**: Save/load complete system states
- **Performance Monitoring**: Real-time FPS and latency tracking

### Advanced Features
- **Hydra Parameter Creation**: Intelligent automatic parameter generation from Hydra code
  - Context-aware naming based on function and chain position
  - RGB color grouping for unified color pickers
  - Instance differentiation for multiple function calls
  - Smart filtering of template references and arrow functions
  - Bidirectional sync between code and TD parameters
  - High-performance with binary search optimization
- **SVG Export**: Vectorization with edge detection for pen plotting
- **AxiDraw Integration**: Direct plotting to AxiDraw via HTTP
- **Parameter Controls**: Slider interface for quick value tweaking

## Quick Start

1. **Open TouchDesigner** and load the HydraTD project
2. **Run QuickStart**: Navigate to `/project1/QuickStart` and click the initialization button
3. **Start Coding**: Edit code in `/hydra_system/code/CodeManager/scene1_code`
4. **See Results**: Watch the Hydra output in `/hydra_system/core/HydraCore/hydra_render`

### Hydra Parameter Creation Quick Start

1. **Write Hydra Code** with numeric values
2. **Run Sync**:
   ```python
   exec(open(r'C:/Users/cuban/HydraToTD/scripts/install_fixed_triggers.py').read())
   sync_now()
   ```
3. **Adjust Parameters** in the HydraParams page
4. **Apply Changes**: Run `apply_now()` to write values back to code

See [documentation/HYDRA_PARAMETER_CREATION.md](documentation/HYDRA_PARAMETER_CREATION.md) for complete guide.

## System Requirements

- **TouchDesigner**: 2023.11xxx or newer
- **Python**: 3.9+ (included with TD)
- **Internet**: Required for Hydra CDN
- **Optional**: Webcam, microphone, AxiDraw plotter

## Installation

### 1. Python Dependencies

```bash
pip install opencv-python numpy requests
```

Optional for WebRTC video streaming:
```bash
pip install aiohttp aiortc
```

### 2. Project Setup

The QuickStart button will automatically:
- Create 4 LFO CHOPs
- Configure DataBridge mappings
- Load 3 example scenes
- Initialize parameters
- Save default preset

### 3. Hydra Parameter Creation Setup

```python
# Install the parameter creation system
exec(open(r'C:/Users/cuban/HydraToTD/scripts/install_fixed_triggers.py').read())
```

Functions available:
- `sync_now()` - Read values from code and create parameters
- `apply_now()` - Write parameter values back to code
- `remove_unused_parameters()` - Clean up unused parameters
- `cleanup_and_sync()` - Remove unused and sync in one step

## Project Structure

```
HydraToTD/
├── /scripts                      - Python scripts
│   ├── manual_triggers_fixed.py  - Hydra Parameter Creation
│   ├── install_fixed_triggers.py - Installer
│   └── /debugging                - Development scripts
├── /documentation                - All documentation
│   ├── HYDRA_PARAMETER_CREATION.md
│   ├── API.md
│   ├── SETUP.md
│   └── [other guides]
├── /presets                      - Saved system states
├── /svg_exports                  - Exported SVG files
└── hydraToTD.toe                - Main TouchDesigner file

TouchDesigner Structure:
/project1
├── /hydra_system
│   ├── /core              - HydraCore (main Hydra engine)
│   ├── /data              - DataBridge (CHOP pipeline)
│   ├── /code              - CodeManager (scene management)
│   ├── /output            - OutputRouter (multi-buffer outputs)
│   ├── AudioBridge        - Audio input handler
│   ├── VideoStreamer      - Video streaming
│   ├── StateManager       - Preset save/load
│   ├── ParameterInterface - UI controls
│   ├── SVGExporter        - Export & plotting
│   ├── direct_param_controller - Parameter creation system
│   └── MasterControl      - Main control panel
└── /QuickStart            - One-button initialization
```

## Usage

### Writing Hydra Code

Edit any scene DAT in CodeManager. In auto mode, changes apply immediately:

```javascript
osc(chop('lfo1', 0) * 20, 0.1, chop('lfo2', 0))
  .rotate(chop('lfo3', 0), 0.1)
  .modulate(noise(chop('lfo4', 0) * 5))
  .out()
```

### Hydra Parameter Creation Workflow

**1. Write code with numeric values:**
```javascript
osc(48, -0.1, 0)
  .color(1.04, 0, -1.1)
  .rotate(3.14, 0.1)
  .out()
```

**2. Sync to create parameters:**
```python
sync_now()
```

This creates:
- `Oscfrequency` = 48
- `Oscsync` = -0.1
- `Oscoffset` = 0
- `Colorrgbone` = RGB(1.04, 0, -1.1) - grouped color picker
- `Rotateangleone` = 3.14
- `Rotatespeedone` = 0.1

**3. Adjust sliders** in TouchDesigner's HydraParams page

**4. Apply changes back to code:**
```python
apply_now()
```

**Parameter Naming Patterns:**
- Source functions: `Oscfrequency`, `Noisescale`
- Chained functions: `Rotateangleone`, `Pixelatepixelytwo`
- Multiple instances: `Oscfrequency`, `Oscfrequencya`, `Oscfrequencyb`
- RGB colors: `Colorrgbone` (unified color picker)

### Available Functions

**CHOP Access:**
- `chop('name', index)` - Access any CHOP channel
- `lfo(1)` - Shorthand for `chop('lfo1', 0)`
- `midi(cc)` - MIDI CC values
- `audioFFT(index)` - Audio analysis bands

**Video Sources:**
- `s0.initCam()` - Initialize webcam
- `s0.initStream(url)` - WebRTC stream
- `src(s0)` - Use video source

**Output Buffers:**
- `.out(o0)` - Main output
- `.out(o1)` - Second output
- `.out(o2)` - Third output
- `.out(o3)` - Fourth output

### Managing Scenes

1. **Switch Scenes**: Modify `scene_registry` active column
2. **Add Scene**: Create new Text DAT and add to registry
3. **Apply Mode**: Toggle between auto/manual in CodeManager
4. **Sync Parameters**: Run `cleanup_and_sync()` when switching scenes

### CHOP Mappings

Add CHOPs to DataBridge registry:

```
chop_path              | enabled | update_rate
/project1/lfo1         | 1       | 30
/project1/audioanalysis| 1       | 60
```

Or use Python:
```python
op('data_bridge').module.addCHOPToRegistry('/project1/my_chop')
```

### Saving Presets

**Save Current State:**
```python
op('/project1/hydra_system/StateManager/preset_manager').module.savePreset('my_preset')
```

**Load Preset:**
```python
op('/project1/hydra_system/StateManager/preset_manager').module.loadPreset('my_preset')
```

Presets include:
- All scene codes
- CHOP mappings
- Parameter values (including HydraParams)
- Active outputs
- Apply mode settings

### SVG Export & Plotting

**Export Frame:**
```python
svg = op('svg_converter').module.captureAndConvert(threshold1=50, threshold2=150)
op('svg_converter').module.saveToFile(svg)
```

**Plot to AxiDraw:**
```python
op('svg_converter').module.captureAndPlot(threshold1=50, threshold2=150)
```

Adjust thresholds for edge detection:
- Lower thresholds = more detail
- Higher thresholds = cleaner lines

## Keyboard Shortcuts (Optional)

If configured in MasterControl:

- `SPACE` - Apply current scene code
- `1/2/3` - Switch to scene 1/2/3
- `S` - Save preset
- `L` - Load preset
- `E` - Export SVG
- `P` - Toggle performance monitor

## Performance Optimization

### Target Metrics
- **Hydra**: 60 FPS
- **CHOP Update**: 30-60 Hz
- **Latency**: <83ms (5 frames @ 60fps)
- **Parameter Sync**: <50ms (optimized with preprocessing)

### Optimization Tips

1. **Reduce CHOP Update Rate**: Lower to 30Hz if experiencing lag
2. **Disable Unused Outputs**: Only enable outputs you're using
3. **Simplify Hydra Code**: Complex effects can impact performance
4. **Lower Resolution**: Reduce Web Render TOP resolution if needed
5. **Batch Parameter Operations**: Use `cleanup_and_sync()` instead of individual calls

## Troubleshooting

### Black Screen in Web Render TOP
- Open Web Inspector (right-click TOP) to check for JavaScript errors
- Verify HTML template loaded correctly
- Check internet connection for Hydra CDN

### CHOPs Not Updating
- Verify CHOP paths in registry are absolute (e.g., `/project1/lfo1`)
- Check CHOP Execute DAT is cooking
- Open Web Inspector console: `console.log(window.tdData)`

### Code Changes Not Applying
- Check apply mode (auto vs manual)
- Look for JavaScript syntax errors in Web Inspector
- Try manual apply button

### Parameter Creation Issues
- **Wrong values**: Run `remove_unused_parameters()` then `sync_now()`
- **Too many parameters**: Check for numbers in arrow functions or templates
- **Parameters not updating**: Verify correct scene is active in scene_registry
- **RGB not grouping**: Ensure `.color()` or `.solid()` values are consecutive

### Poor Performance
- Reduce CHOP update rate in DataBridge
- Disable unused outputs in OutputRouter
- Simplify Hydra code
- Lower Web Render TOP resolution

### SVG Export Issues
- Adjust threshold sliders (try 100/200 for cleaner lines)
- Simplify Hydra output (higher contrast works better)
- Check exports folder for saved files

### AxiDraw Not Responding
- Ensure Python server is running: `python axidraw_server.py`
- Verify server at http://localhost:8000
- Check AxiDraw USB connection

## Documentation

Complete documentation available in `/documentation`:

### Getting Started
- [SETUP.md](documentation/SETUP.md) - Installation and setup guide
- [API.md](documentation/API.md) - Complete API reference

### Feature Guides
- [HYDRA_PARAMETER_CREATION.md](documentation/HYDRA_PARAMETER_CREATION.md) - Parameter creation system
- [MULTI_OUTPUT_SYSTEM.md](documentation/MULTI_OUTPUT_SYSTEM.md) - Multi-buffer output guide
- [SVG_EXPORT_SYSTEM.md](documentation/SVG_EXPORT_SYSTEM.md) - SVG export and plotting
- [PRESET_SYSTEM.md](documentation/PRESET_SYSTEM.md) - Preset save/load system

### Implementation
- [Architechure.md](documentation/Architechure.md) - System architecture
- [Hydra-TouchDesigner Implementation Blueprint.md](documentation/Hydra-TouchDesigner%20Implementation%20Blueprint.md) - Build guide
- [Hydra-TouchDesigner Technical Stack.md](documentation/Hydra-TouchDesigner%20Technical%20Stack.md) - Technical specifications

## Examples

The project includes example scenes:
- **Scene 1**: LFO reactive patterns
- **Scene 2**: Colorful noise with kaleidoscope
- **Scene 3**: Feedback loop effects

Example presets in `/presets/examples`:
- `audio_reactive.json` - Audio-driven visuals
- `video_feedback.json` - Video processing
- `generative.json` - Autonomous animation

## Development

### Project Phases

**Phase 1 (Core) ✓**
- HydraCore with basic rendering
- DataBridge with CHOP integration
- CodeManager with scene switching
- QuickStart preset

**Phase 2 (Streaming) ✓**
- VideoStreamer with WebRTC
- AudioBridge with dual input
- Latency optimization

**Phase 3 (Advanced) ✓**
- OutputRouter (4 outputs)
- StateManager (presets)
- ParameterInterface (UI)
- SVGExporter + AxiDraw

**Phase 4 (Parameter Automation) ✓**
- Hydra Parameter Creation system
- Intelligent naming and grouping
- Bidirectional sync
- Performance optimization

### Contributing

Scripts organized in `/scripts`:
- Production scripts in `/scripts`
- Development/debug scripts in `/scripts/debugging`

See [CLAUDE.md](documentation/CLAUDE.md) for development guidelines.

## Known Limitations

1. **Web Render TOP**: Limited to one Chromium instance per TOP
2. **WebRTC Latency**: Minimum 2-3 frame delay
3. **CHOP Updates**: `executeJavaScript()` adds overhead
4. **SVG Quality**: Edge detection is lossy
5. **Platform Differences**: Some features vary on Mac/Windows
6. **Parameter Detection**: Cannot detect values in expressions or arrow functions

## Future Enhancements

- GLSL shader injection
- OSC network control
- Multi-user collaboration
- Cloud preset storage
- Real-time video recording
- Mobile interface for live performance
- Parameter animation recording
- Custom parameter name templates

## Resources

- **Hydra**: https://hydra.ojack.xyz/
- **TouchDesigner**: https://docs.derivative.ca/
- **AxiDraw**: https://axidraw.com/
- **Project Repository**: [Your repository URL]

## License

This project integrates:
- Hydra-Synth (AGPL-3.0)
- TouchDesigner (Commercial/Educational)

## Credits

Created for live coding and generative art workflows.
Combines the power of Hydra's visual synthesis with TouchDesigner's data processing.

Special thanks to:
- Olivia Jack for Hydra
- Derivative for TouchDesigner
- The generative art community

---

**Version**: 1.5
**Last Updated**: 2025-10-20
**Status**: Production Ready
