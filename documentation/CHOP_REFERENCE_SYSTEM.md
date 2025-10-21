# Universal CHOP Reference System

**Status:** ✅ Fully Operational

---

## Overview

You can now reference ANY CHOP in your TouchDesigner project directly in Hydra code using template syntax. This includes LFOs, mouse input, null CHOPs, audio analysis, and any custom CHOPs you create.

---

## Template Syntax

### LFO CHOPs (Original)
```javascript
{{lfo1}}, {{lfo2}}, {{lfo3}}, {{lfo4}}
```

### Mouse Input
```javascript
{{mouse.x}}  // Mouse tx channel (-1 to 1)
{{mouse.y}}  // Mouse ty channel (-1 to 1)
```

### Universal CHOP Reference
```javascript
{{chopname.channel}}
```

Where:
- `chopname` = CHOP operator name
- `channel` = Channel index (0, 1, 2...) OR channel name (tx, ty, r, etc.)

---

## Examples

### Basic CHOP References

```javascript
// Null CHOP with 3 channels
{{null1.0}}     // First channel (index 0)
{{null1.1}}     // Second channel (index 1)
{{null1.2}}     // Third channel (index 2)

// Audio CHOP
{{audioin1.0}}  // Left channel
{{audioin1.1}}  // Right channel

// Transform CHOP
{{transform1.tx}}  // X translation channel
{{transform1.ty}}  // Y translation channel
{{transform1.r}}   // Rotation channel
```

### Hydra Patterns

#### Mouse-Reactive Pattern
```javascript
osc({{lfo1}} * 20, 0.1, ({{mouse.x}} + 1) * 0.5)
  .rotate({{mouse.y}} * 3.14)
  .out()
```

#### Null CHOP Color Control
```javascript
solid({{null1.0}}, {{null1.1}}, {{null1.2}})
  .kaleid({{lfo1}} * 8)
  .out()
```

#### Mixed Control
```javascript
noise({{lfo1}} * 5)
  .scale({{mouse.x}} * 0.5 + 1)
  .rotate({{null5.0}} * 3.14)
  .modulateScale(osc(10), {{lfo2}} * 0.5)
  .out()
```

---

## CHOP Lookup Order

The system searches for CHOPs in this order:

1. `/project1/chopname`
2. `/project1/hydra_system/chopname`
3. `/chopname` (absolute path)

**Example:** `{{null5.0}}`
- First checks: `/project1/null5`
- Then checks: `/project1/hydra_system/null5`
- Finally checks: `/null5`

---

## Error Handling

### Helpful Error Messages

The system now provides clear error messages when something goes wrong:

```
⚠️  {{null5.1}}: Channel index 1 out of range (CHOP has 1 channels)
⚠️  {{audio.3}}: Channel index 3 out of range (CHOP has 2 channels)
⚠️  {{mynull.tx}}: Channel 'tx' not found
⚠️  {{missing.0}}: CHOP 'missing' not found
```

### Common Issues

**Issue:** "Channel index 1 out of range (CHOP has 1 channels)"
- **Solution:** Channel indices start at 0, not 1. Use `{{null5.0}}` instead of `{{null5.1}}`

**Issue:** "Channel 'chan1' not found"
- **Solution:** Use the channel index instead: `{{null5.0}}`

**Issue:** "CHOP 'mynull' not found"
- **Solution:** Check CHOP exists and path is correct. Create it if needed.

---

## Mouse Input Details

### Mouse Channels

The `mousein1` CHOP provides:
- `tx` → mapped to `{{mouse.x}}` (-1 to 1)
- `ty` → mapped to `{{mouse.y}}` (-1 to 1)

### Converting Mouse Range

Mouse values range from **-1 to 1**. To convert to **0 to 1**:

```javascript
// Convert -1 to 1 → 0 to 1
({{mouse.x}} + 1) * 0.5

// Example usage
osc(10, 0.1, ({{mouse.x}} + 1) * 0.5)
  .rotate(({{mouse.y}} + 1) * 3.14)
  .out()
```

---

## Creating Control CHOPs

### Example: 3-Channel Color Control

```python
# Create null CHOP for RGB control
color_null = op('/project1').create(nullCHOP, 'color_control')

# Add 3 constant CHOPs for R, G, B
r_const = op('/project1').create(constantCHOP, 'color_r')
r_const.par.value0 = 1.0

g_const = op('/project1').create(constantCHOP, 'color_g')
g_const.par.value0 = 0.5

b_const = op('/project1').create(constantCHOP, 'color_b')
b_const.par.value0 = 0.0

# Merge into null
merge = op('/project1').create(mergeCHOP, 'color_merge')
merge.par.chop0 = 'color_r'
merge.par.chop1 = 'color_g'
merge.par.chop2 = 'color_b'

color_null.par.chop = 'color_merge'
```

**Use in Hydra:**
```javascript
solid({{color_control.0}}, {{color_control.1}}, {{color_control.2}})
  .out()
```

---

## Audio Reactivity Example

### Setup Audio Input

```python
# Create audio device in CHOP
audio = op('/project1').create(audioDeviceIn, 'audioin1')
audio.par.device = 'Microphone'
```

**Use in Hydra:**
```javascript
// Audio-reactive oscillator
osc({{audioin1.0}} * 50 + 10, 0.1)
  .modulate(noise({{audioin1.1}} * 10))
  .out()
```

---

## Advanced: Custom CHOP Networks

### Example: Beat Detection

```python
# Audio in → FFT → Beat detection
audio = op('/project1/audioin1')

# Analyze low frequencies for kick drum
analyze = op('/project1').create(analyzeCHOP, 'beat_detect')
analyze.par.chop = 'audioin1'
analyze.par.function = 'average'

# Use in Hydra
```

```javascript
osc({{lfo1}} * 20)
  .scale({{beat_detect.0}} * 2 + 1)  // Pulse with beat
  .out()
```

---

## Performance Tips

### CHOP Registry

CHOPs in the registry update at specified rates:

```python
# Check CHOP registry
registry = op('/project1/hydra_system/data/DataBridge/chop_registry')

# Current registered CHOPs:
# /project1/lfo1        - 60fps
# /project1/lfo2        - 60fps
# /project1/lfo3        - 60fps
# /project1/lfo4        - 60fps
# /project1/mousein1    - 60fps
```

### Update Rates

- **LFOs:** Already in registry, update automatically
- **Mouse:** Added to registry at 60fps
- **Custom CHOPs:** Reference directly (no registry needed)

---

## Complete Example: Interactive Art Piece

### TouchDesigner Setup

```python
# Create control CHOPs
speed = op('/project1').create(constantCHOP, 'speed')
speed.par.value0 = 1.0

complexity = op('/project1').create(constantCHOP, 'complexity')
complexity.par.value0 = 4.0

color_shift = op('/project1').create(constantCHOP, 'color_shift')
color_shift.par.value0 = 0.5
```

### Hydra Code

```javascript
// Interactive generative pattern
osc({{lfo1}} * {{speed.0}} * 20, 0.1, {{color_shift.0}})
  .rotate({{mouse.y}}, {{lfo2}} * 0.1)
  .kaleid({{complexity.0}})
  .scale({{mouse.x}} * 0.5 + 1)
  .modulateRotate(
    noise({{lfo3}} * 3),
    {{lfo4}} * 0.5
  )
  .out()
```

**Result:** Move mouse to control scale/rotation, adjust speed/complexity/color via sliders

---

## Keyboard Shortcuts (Updated)

**ALL shortcuts now require CTRL+SHIFT** to prevent accidental triggers while typing:

| Shortcut | Action |
|----------|--------|
| **CTRL+SHIFT+1/2/3** | Switch scenes |
| **CTRL+SHIFT+R** | Reload Hydra page |
| **CTRL+SHIFT+B** | Apply scene manually |
| **CTRL+SHIFT+S** | Save as 'default' preset |
| **CTRL+SHIFT+L** | Load 'default' preset |
| **CTRL+SHIFT+E** | Export SVG (placeholder) |
| **CTRL+SHIFT+M** | Performance monitor (placeholder) |

---

## Summary

### What You Can Reference

✅ LFO CHOPs - `{{lfo1}}` through `{{lfo4}}`
✅ Mouse Input - `{{mouse.x}}`, `{{mouse.y}}`
✅ Null CHOPs - `{{null1.0}}`, `{{mynull.tx}}`
✅ Audio Input - `{{audioin1.0}}`
✅ Custom CHOPs - Any CHOP in your project
✅ By Index - `{{chop.0}}`, `{{chop.1}}`
✅ By Name - `{{chop.tx}}`, `{{chop.chan1}}`

### Next Steps

1. **Create control CHOPs** - Use null, constant, or math CHOPs
2. **Reference in Hydra** - Use `{{chopname.channel}}` syntax
3. **Test patterns** - Move mouse, adjust sliders, watch real-time updates
4. **Save presets** - CTRL+SHIFT+S to save your setup

---

**System Status:** ✅ Universal CHOP Reference Working
**Mouse Support:** ✅ Active
**Error Handling:** ✅ Helpful Messages
**Last Updated:** 2025-10-11
