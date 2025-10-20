# Hydra-TouchDesigner Integration - FINAL WORKING SYSTEM

## Status: ✅ FULLY OPERATIONAL

Real-time LFO control of Hydra patterns with efficient scene switching!

---

## What's Working

✅ **Real-time LFO control** - Change LFO parameters and see immediate updates
✅ **Fast scene switching** - Switch between scenes with keyboard (1/2/3)
✅ **Template-based code** - Inject LFO values into Hydra code
✅ **Efficient updates** - Updates every 6 frames (~10fps) for smooth performance
✅ **No memory leaks** - Stable performance, no crashes
✅ **Keyboard shortcuts** - Quick scene control and manual updates

---

## System Architecture

```
LFO CHOPs → Code Generator → Template Injection → Hydra Execution
    ↓            ↓                 ↓                    ↓
/project1/   Reads current    Replaces {{lfo1}}    Web Render TOP
lfo1-4       LFO values       with 0.543           displays pattern
```

**Update Loop:**
1. Constant CHOP changes every 6 frames (`absTime.frame % 6`)
2. CHOP Execute DAT triggers `onValueChange`
3. Code generator reads current LFO values
4. Template `{{lfo1}}` → actual value `0.543`
5. Generated code executes in Hydra
6. Pattern updates with new values

---

## Hydra Scene Template Syntax

### Basic Usage

Use `{{lfoX}}` where X is 1-4:

```javascript
// Direct value
osc({{lfo1}} * 20 + 10, 0.1, {{lfo2}})

// In rotation
.rotate({{lfo3}} * 3.14, 0.1)

// In modulation
.modulate(noise({{lfo4}} * 5))

// In color
.color({{lfo1}}, {{lfo2}}, {{lfo3}})

// As kaleid parameter
.kaleid({{lfo1}} * 8)
```

### Example Scenes

**Scene 1** (multi-LFO control):
```javascript
osc({{lfo1}} * 20 + 10, 0.1, {{lfo2}})
  .rotate({{lfo3}} * 3.14, 0.1)
  .modulate(noise({{lfo4}} * 5))
  .out()
```

**Scene 2** (color control):
```javascript
noise({{lfo1}} * 5, 0.1)
  .color({{lfo2}}, {{lfo3}}, {{lfo4}})
  .kaleid(8)
  .out()
```

**Scene 3** (simple):
```javascript
osc(10, 0.1, 1.4)
  .rotate({{lfo1}}, 0.1)
  .modulate(noise({{lfo3}} * 3), {{lfo2}} * 0.5)
  .out()
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **1** | Switch to Scene 1 |
| **2** | Switch to Scene 2 |
| **3** | Switch to Scene 3 |
| **CTRL+SHIFT+B** | Manually apply active scene |
| **R** | Reload Hydra page |

**Placeholder keys** (not yet implemented):
- **S** - Save preset
- **L** - Load preset
- **E** - Export SVG
- **M** - Performance monitor

---

## Key Components

### DataBridge (`/project1/hydra_system/data/DataBridge/`)

- **code_generator** (Text DAT) - Injects LFO values into templates
- **update_trigger1** (Constant CHOP) - Expression: `absTime.frame % 6`
- **template_updater** (CHOP Execute DAT) - Triggers code generation
- **data_collector** (Text DAT) - Contains `data_bridge.py` module
- **chop_registry** (Table DAT) - Lists monitored CHOPs

### CodeManager (`/project1/hydra_system/code/CodeManager/`)

- **code_executor** (Text DAT) - Contains `code_manager.py` module
- **scene1_code** (Text DAT) - Scene 1 template
- **scene2_code** (Text DAT) - Scene 2 template
- **scene3_code** (Text DAT) - Scene 3 template
- **scene_registry** (Table DAT) - Tracks active scene

### Controls (`/project1/hydra_system/controls/`)

- **keyboard_in** (Keyboard In CHOP) - Captures key presses
- **key_handler** (CHOP Execute DAT) - Handles keyboard events

### HydraCore (`/project1/hydra_system/core/HydraCore/`)

- **hydra_render** (Web Render TOP) - Displays Hydra visuals
- **URL:** `html/hydra_clean.html`

---

## LFO Control

### Real-Time Parameter Control

Change LFO parameters in TouchDesigner UI or via Python:

```python
# Change offset (immediate visual change)
op('/project1/lfo1').par.offset = 0.8

# Change amplitude (scale/intensity)
op('/project1/lfo3').par.amp = 2.0

# Change frequency (animation speed)
op('/project1/lfo1').par.frequency = 3.0

# Important: Keep reset OFF!
op('/project1/lfo1').par.reset = 0
```

### LFO Configuration

- **LFO1-4:** `/project1/lfo1` through `/project1/lfo4`
- **Type:** LFO CHOP
- **Reset:** Must be OFF for animation
- **Registered:** in `chop_registry` table

---

## Performance

**Update Rate:** ~10fps (every 6 frames)
**Scene Switch:** Instant (no re-compilation)
**Memory:** Stable (no leaks)
**CPU:** Low impact

### Performance Tips

- Lower update rate: Change `absTime.frame % 6` to `% 12` (slower updates, less CPU)
- Higher update rate: Change to `% 3` (faster updates, more CPU)
- Avoid complex feedback loops for best performance

---

## Troubleshooting

### Scene won't load
```python
# Reload Hydra page
op('/project1/hydra_system/core/HydraCore/hydra_render').par.reload.pulse()

# Or press R key
```

### LFO changes don't update pattern
```python
# Check if update trigger is active
updater = op('/project1/hydra_system/data/DataBridge/template_updater')
print(f"Active: {updater.par.active.eval()}")
print(f"CHOP: {updater.par.chop.eval()}")

# Should show:
# Active: True
# CHOP: update_trigger1 (or update_trigger2)
```

### Pattern frozen
```python
# Check Constant CHOP is changing
trigger = op('/project1/hydra_system/data/DataBridge/update_trigger1')
print(trigger.chan(0)[0])
# Wait a moment, run again - value should change
```

### Scene has syntax error
- Check template uses `{{lfo1}}` not `chop('lfo1', 0)()`
- Make sure all parentheses are balanced
- Test scene code in browser Hydra editor first

---

## Setup Scripts

All scripts in `C:\Users\cuban\HydraToTD\scripts\`:

- **chop_to_dat_fixed.py** - Sets up template system
- **cleanup_and_add_error_handling.py** - Clean output, error handling
- **fix_scene2.py** - Convert scene to template format
- **optimize_performance.py** - Adjust update rate

---

## Known Limitations

1. **No return values from Hydra** - Can't read data back from Web Render TOP
2. **Feedback loops** - `.modulate(o0)` can be slow with continuous updates
3. **Update latency** - ~0.1s delay between LFO change and visual update
4. **No Hydra console access** - Can't see JavaScript errors in TD

---

## Future Enhancements

**Phase 2:**
- [ ] Video streaming (WebRTC input)
- [ ] Audio reactivity (FFT → Hydra)
- [ ] Multi-output routing
- [ ] Preset save/load system

**Phase 3:**
- [ ] SVG export for AxiDraw
- [ ] MIDI control integration
- [ ] OSC input support
- [ ] Performance monitor display

---

## Technical Details

### Template Replacement

Template: `osc({{lfo1}} * 20, ...)`
LFO1 value: `0.543216`
Generated: `osc(0.543216 * 20, ...)`

### Code Flow

1. User changes LFO → LFO CHOP outputs new value
2. Constant CHOP cycles → CHOP Execute fires
3. Code generator reads LFO values
4. Template string replacement
5. Execute generated code in Hydra
6. Web Render TOP displays result

### Why This Works

- ✅ Code executes once with numeric values (not functions)
- ✅ No continuous re-execution (just new values)
- ✅ Hydra evaluates numeric expressions efficiently
- ✅ No feedback loop re-compilation issues

---

**System Status:** Fully operational
**Performance:** Excellent
**Last Updated:** 2025-10-10

🎉 **Phase 1 Complete!** Real-time Hydra-TouchDesigner integration working perfectly!
