# Preset System - Phase 2

**Status:** ✅ Ready to Deploy

---

## Overview

The preset system allows you to save and load complete system states including:
- All scene codes (Scene 1, 2, 3)
- LFO parameter values (frequency, amplitude, offset, phase)
- Active scene selection

---

## Installation

Run this script in TouchDesigner textport:

```python
exec(open('C:/Users/cuban/HydraToTD/scripts/setup_preset_system.py').read())
```

This will:
1. Create `/project1/hydra_system/presets/PresetManager/` base
2. Add `state_manager` module for save/load functions
3. Create `preset_list` table to track presets
4. Update keyboard handler with S/L shortcuts

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **S** | Quick save with timestamp (e.g., `preset_20251011_143022.json`) |
| **L** | Load most recent preset |
| **CTRL+S** | Save as 'default' preset |
| **CTRL+L** | Load 'default' preset |

---

## Usage

### Quick Save/Load Workflow

1. **Create your scene** - Adjust LFOs, write Hydra code
2. **Press S** - Instantly saves current state with timestamp
3. **Make changes** - Experiment with different settings
4. **Press L** - Instantly returns to your last saved state

### Default Preset Workflow

1. **Set up your favorite configuration**
2. **Press CTRL+S** - Saves as 'default' preset
3. **Anytime later, press CTRL+L** - Instantly loads your default setup

---

## What Gets Saved

### Scene Codes
```javascript
// All scene code is saved exactly as written
osc({{lfo1}} * 20 + 10, 0.1, {{lfo2}})
  .rotate({{lfo3}} * 3.14, 0.1)
  .modulate(noise({{lfo4}} * 5))
  .out()
```

### LFO Parameters
- Frequency
- Amplitude
- Offset
- Phase

### Active Scene
- Which scene (1, 2, or 3) is currently active

---

## Preset Storage

Presets are saved as JSON files in:
```
{project_folder}/presets/
```

### Preset File Format

```json
{
  "version": "1.0",
  "name": "preset_20251011_143022",
  "timestamp": "2025-10-11T14:30:22.123456",
  "scenes": {
    "scene1": {
      "code": "osc({{lfo1}} * 20, 0.1).out()",
      "active": true
    },
    "scene2": {
      "code": "noise({{lfo2}} * 5).out()",
      "active": false
    },
    "scene3": {
      "code": "solid(1).out()",
      "active": false
    }
  },
  "lfo_values": {
    "lfo1": {
      "frequency": 1.0,
      "amplitude": 1.0,
      "offset": 0.5,
      "phase": 0.0
    },
    "lfo2": { ... },
    "lfo3": { ... },
    "lfo4": { ... }
  },
  "active_scene": "scene1"
}
```

---

## Python API

### Save Preset

```python
# Quick save with timestamp
state_manager = op('/project1/hydra_system/presets/PresetManager/state_manager')
state_manager.module.savePreset()

# Save with custom name
state_manager.module.savePreset('my_favorite_pattern')
```

### Load Preset

```python
# Load specific preset
state_manager.module.loadPreset('my_favorite_pattern')

# Load most recent
state_manager.module.loadMostRecent()
```

### List Presets

```python
# Print all available presets
presets = state_manager.module.listPresets()

# Returns list of dicts:
# [{'name': 'preset_20251011_143022', 'timestamp': '2025-10-11T14:30:22', 'path': '...'}]
```

---

## Component Structure

```
/project1/hydra_system/presets/
└── PresetManager/
    ├── state_manager      (Text DAT) - Save/load module
    ├── preset_list        (Table DAT) - Available presets
    └── current_preset     (Text DAT) - Current preset name
```

---

## Workflow Examples

### Example 1: Iterative Design

```
1. Press S - Save starting point
2. Tweak LFO1 frequency
3. Press S - Save variation 1
4. Tweak LFO2 amplitude
5. Press S - Save variation 2
6. Press L repeatedly - Cycle through recent saves to compare
```

### Example 2: Performance Setup

```
1. Create Scene 1 (intro pattern)
2. Adjust LFOs for intro
3. Press CTRL+S - Save as 'default'

During performance:
- Press 2 - Switch to Scene 2
- Press L - Return to last state
- Press CTRL+L - Return to default intro
```

### Example 3: A/B Comparison

```
1. Set up version A
2. Press S - Save A
3. Make drastic changes (version B)
4. Press L - Back to A
5. Make more changes (version C)
6. Press L - Back to B
7. Press L again - Back to A
```

---

## Troubleshooting

### Preset not saving

```python
# Check if PresetManager exists
pm = op('/project1/hydra_system/presets/PresetManager')
print("PresetManager exists:", pm is not None)

# Check if state_manager module is loaded
sm = pm.op('state_manager')
print("Module loaded:", hasattr(sm, 'module'))
```

### Preset not loading

```python
# List available presets
state_manager = op('/project1/hydra_system/presets/PresetManager/state_manager')
state_manager.module.listPresets()

# Check preset file exists
import pathlib
preset_dir = pathlib.Path(project.folder) / 'presets'
print("Presets:", list(preset_dir.glob('*.json')))
```

### Keyboard shortcut not working

```python
# Check key handler
key_handler = op('/project1/hydra_system/controls/key_handler')
print("Handler text length:", len(key_handler.text))
print("Has 's' key handler:", "'s'" in key_handler.text)

# Manually trigger save
state_manager = op('/project1/hydra_system/presets/PresetManager/state_manager')
state_manager.module.savePreset('test')
```

---

## Advanced Usage

### Preset Organization

Organize presets by naming convention:

```python
# Performance presets
state_manager.module.savePreset('show1_intro')
state_manager.module.savePreset('show1_buildup')
state_manager.module.savePreset('show1_climax')

# Experimental presets
state_manager.module.savePreset('exp_feedback_loops')
state_manager.module.savePreset('exp_kaleidoscope')
```

### Batch Operations

```python
# Export all presets to specific folder
import shutil
from pathlib import Path

preset_dir = Path(project.folder) / 'presets'
backup_dir = Path(project.folder) / 'preset_backups' / '2025-10-11'
backup_dir.mkdir(parents=True, exist_ok=True)

for preset_file in preset_dir.glob('*.json'):
    shutil.copy(preset_file, backup_dir / preset_file.name)

print(f"Backed up {len(list(preset_dir.glob('*.json')))} presets")
```

### Preset Morphing (Future Enhancement)

```python
# TODO: Interpolate between two presets
# state_manager.module.morphPresets('preset_a', 'preset_b', 0.5)
```

---

## Limitations

1. **No scene template changes** - Presets save scene code, but if you change the template structure (e.g., add new scenes), old presets won't include them
2. **No UI state** - Custom UI positions, window layouts not saved
3. **No external dependencies** - External video sources, audio inputs not saved
4. **No output routing** - Output selection (o0-o3) not saved (Phase 3 feature)

---

## Future Enhancements (Phase 3)

- [ ] Preset browser UI with thumbnails
- [ ] Preset categories and tags
- [ ] Preset morphing/interpolation
- [ ] Cloud sync for presets
- [ ] Preset export/import (.zip bundles)
- [ ] Version control integration

---

**System Status:** Phase 2 Complete ✅
**Preset System:** Ready to Use ✅
**Last Updated:** 2025-10-11
