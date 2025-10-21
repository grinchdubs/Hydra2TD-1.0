# Hydra-TouchDesigner Integration

A complete system for running the Hydra live coding environment inside TouchDesigner with full bidirectional data flow, enabling new generative art workflows.

## Features

### Core System
- **Hydra Engine**: Full Hydra-Synth running in Web Render TOP
- **CHOP Integration**: Access any TouchDesigner CHOP via `{{chopname.index}}` function
- **Multi-Scene Management**: Switch between multiple Hydra code scenes
- **Audio Reactivity**: Dual audio input (Hydra built-in + TD analysis)
- **Multi-Output**: 4 independent output buffers (o0-o3)
- **Preset System**: Save/load complete system states

### Advanced Features
- **Hydra Parameter Creation**: Intelligent automatic parameter generation from Hydra code
  - Context-aware naming based on function and chain position
  - RGB color grouping for unified color pickers
  - Instance differentiation for multiple function calls
  - Smart filtering of template references and arrow functions
  - Bidirectional sync between code and TD parameters
  - High-performance with binary search optimization
- **Parameter Controls**: Slider interface for quick value tweaking

## Quick Start

1. **Open TouchDesigner** and load the HydraTD project
3. **Start Coding**: Connect a textDAT to 1 of the 3 scenes in `Hydra Code Examples` section and start editing in the editor window provided below
4. **See Results**: Watch the Hydra output in the `Hydra_out` TOP or with the `Hydra Viewer` button. You can also open the Hydra editor window but clicking the `View Hydra Editor` button for a more traditional Hydra experience.

### Hydra Parameter Creation Quick Start

1. **Write Hydra Code** with numeric values
2. **Sync** click outside the editor to sync automatically
3. **Adjust Parameters** in the HydraParams page

See [documentation/HYDRA_PARAMETER_CREATION.md](documentation/HYDRA_PARAMETER_CREATION.md) for complete guide.

## System Requirements

- **TouchDesigner**: 2023.11xxx or newer
- **Internet**: Required for Hydra CDN

## Usage

### Writing Hydra Code

Edit any scene textDAT in the project comp and connect it to one of the 3 scenes. In auto mode, changes apply immediately:

```javascript
osc({{lfo1}} * 20, 0.1, {{lfo2}})
  .rotate({{lfo3}}, 0.1)
  .modulate(noise({{lfo4}} * 5))
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

**2. Adjust sliders** in TouchDesigner's HydraParams page
The code should auto update after any slider movements.

### Available Functions

**CHOP Access:**
- `{{chopname.index}}` - Access any CHOP channel {{}}
- `{{lfo1}}` - LFO1 value 
- `{{null1.1}}` - Null1 value at index 1
- `{{{{mouse.x}}}}` - Mousein1 X value

**Output Buffers:**
- `.out(o0)` - Main output
- `.out(o1)` - Second output
- `.out(o2)` - Third output
- `.out(o3)` - Fourth output

### Managing Scenes

1. **Switch Scenes**: use key commands or connect an example. see `Hydra code examples` section
2. **Add Scene**: Create new Text DAT and connect it to 1 of the 3 scenes
3. **Sync**: Parameter window should automatically on scene change.

## Keyboard Shortcuts

- `CTRL+SHIFT+1/2/3` - Switch to scene 1/2/3
- `CTRL+SHIFT+S` - Save preset
- `CTRL+SHIFT+L` - Load preset

### Saving Presets
Presets include:
- All scene codes
- CHOP mappings
- Parameter values (including HydraParams)
- Active outputs
- Apply mode settings


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

## Documentation

Complete documentation available in `/documentation`:

### Getting Started
- [SETUP.md](documentation/SETUP.md) - Installation and setup guide
- [API.md](documentation/API.md) - Complete API reference

### Feature Guides
- [HYDRA_PARAMETER_CREATION.md](documentation/HYDRA_PARAMETER_CREATION.md) - Parameter creation system
- [MULTI_OUTPUT_SYSTEM.md](documentation/MULTI_OUTPUT_SYSTEM.md) - Multi-buffer output guide
- [PRESET_SYSTEM.md](documentation/PRESET_SYSTEM.md) - Preset save/load system
- [CHOP_REFERENCE_SYSTEM.md](documentation/CHOP_REFERENCE_SYSTEM.md) - Chop Reference System

## Examples

The project includes example scenes:
- **Scene 1**: LFO reactive patterns
- **Scene 2**: Colorful noise with kaleidoscope
- **Scene 3**: Feedback loop effects


## Known Limitations

1. **Web Render TOP**: Limited to one Chromium instance per TOP
2. **WebRTC Latency**: Minimum 2-3 frame delay
3. **CHOP Updates**: `executeJavaScript()` adds overhead
4. **Platform Differences**: Some features vary on Mac/Windows
5. **Parameter Detection**: Cannot detect values in expressions or arrow functions

## Future Enhancements

- GLSL shader injection
- Real-time video recording

## Resources

- **Hydra**: https://hydra.ojack.xyz/
- **TouchDesigner**: https://docs.derivative.ca/
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

**Version**: 1.0
**Last Updated**: 2025-10-20
**Status**: Production Ready
