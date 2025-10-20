# Hydra-TouchDesigner Examples

Collection of example code snippets and use cases for the Hydra-TouchDesigner integration.

## Table of Contents

- [Basic Patterns](#basic-patterns)
- [CHOP Integration](#chop-integration)
- [Audio Reactive](#audio-reactive)
- [Video Processing](#video-processing)
- [Multi-Output](#multi-output)
- [Pen Plotting](#pen-plotting)
- [Advanced Techniques](#advanced-techniques)

---

## Basic Patterns

### Simple Oscillator
```javascript
osc(10, 0.1, 1.4).out()
```

### Colorful Noise
```javascript
noise(3, 0.1)
  .color(1, 0.5, 0.8)
  .out()
```

### Geometric Shapes
```javascript
shape(4, 0.5, 0.01)
  .repeat(3, 3)
  .out()
```

### Kaleidoscope Effect
```javascript
voronoi(5, 0.3, 0.2)
  .kaleid(6)
  .out()
```

---

## CHOP Integration

### Using LFOs
```javascript
// Single LFO controlling frequency
osc(chop('lfo1', 0) * 20 + 10, 0.1, 1).out()

// Multiple LFOs
osc(
  chop('lfo1', 0) * 20,
  chop('lfo2', 0) * 0.5,
  chop('lfo3', 0)
).out()
```

### Shorthand LFO Access
```javascript
// Using lfo() helper function
osc(lfo(1) * 20, 0.1, lfo(2)).out()
```

### Color Control
```javascript
noise(3, 0.1)
  .color(
    chop('lfo1', 0),
    chop('lfo2', 0),
    chop('lfo3', 0)
  )
  .out()
```

### Rotation and Scale
```javascript
shape(4)
  .rotate(chop('lfo1', 0) * 3.14, 0.1)
  .scale(chop('lfo2', 0) * 2 + 0.5)
  .out()
```

### Modulation
```javascript
osc(10, 0.1, 1)
  .modulate(
    noise(chop('lfo1', 0) * 5),
    chop('lfo2', 0) * 0.5
  )
  .out()
```

---

## Audio Reactive

### Using Hydra's Built-in Audio
```javascript
// Enable audio in Hydra initialization
// Then use a.fft[index]

osc(10, 0.1, () => a.fft[0])
  .modulate(noise(() => a.fft[1] * 5))
  .out()
```

### Using TouchDesigner Audio Analysis
```javascript
// Requires Audio Spectrum CHOP named 'audio_spectrum'

osc(10, 0.1, audioFFT(0) * 5)
  .color(
    audioFFT(0),
    audioFFT(1),
    audioFFT(2)
  )
  .out()
```

### Bass-Reactive Shapes
```javascript
shape(() => a.fft[0] * 6 + 3, 0.5, 0.01)
  .repeat(() => a.fft[1] * 3 + 1, () => a.fft[2] * 3 + 1)
  .out()
```

### Frequency-Based Colors
```javascript
gradient(() => a.fft[0])
  .color(
    () => a.fft[0],
    () => a.fft[1],
    () => a.fft[2]
  )
  .kaleid(4)
  .out()
```

### Waveform Visualization
```javascript
// Using multiple FFT bands
voronoi(() => a.fft[0] * 10, () => a.fft[1], () => a.fft[2])
  .thresh(() => a.fft[3] * 0.5)
  .invert()
  .out()
```

---

## Video Processing

### Webcam Input
```javascript
// Initialize webcam
s0.initCam()

// Display with effects
src(s0)
  .kaleid(4)
  .out()
```

### Video Feedback Loop
```javascript
s0.initCam()

src(s0)
  .modulate(o0, 0.05)
  .scale(1.01)
  .rotate(0.001)
  .out()
```

### Difference Effect
```javascript
s0.initCam()

src(s0)
  .diff(o0)
  .modulate(noise(3))
  .out()
```

### Color Manipulation
```javascript
s0.initCam()

src(s0)
  .color(
    chop('lfo1', 0),
    chop('lfo2', 0),
    chop('lfo3', 0)
  )
  .contrast(1.5)
  .out()
```

### Blending with Patterns
```javascript
s0.initCam()

src(s0)
  .blend(
    osc(10, 0.1, 1),
    chop('lfo1', 0) * 0.5
  )
  .out()
```

---

## Multi-Output

### Different Patterns on Each Output
```javascript
// Output 0: Oscillator
osc(10, 0.1, 1).out(o0)

// Output 1: Noise
noise(3).out(o1)

// Output 2: Shapes
shape(4).out(o2)

// Output 3: Voronoi
voronoi(5).out(o3)
```

### Cross-Buffer Modulation
```javascript
// o0 modulates o1
osc(10).out(o0)
noise(3).modulate(o0, 0.5).out(o1)

// o1 blends with o2
shape(4).blend(o1, 0.5).out(o2)

// o2 and o3 mixed
voronoi(5).add(o2, 0.5).out(o3)
```

### Layer Compositing
```javascript
// Background layer
gradient(1).out(o0)

// Pattern layer
osc(chop('lfo1', 0) * 20).out(o1)

// Composite
src(o0)
  .add(o1, chop('lfo2', 0) * 0.5)
  .out(o2)
```

---

## Pen Plotting

### High-Contrast Patterns
```javascript
// Simple lines
osc(20, 0)
  .thresh(0.5, 0.01)
  .invert()
  .out()
```

### Geometric Designs
```javascript
// Clean shapes for plotting
shape(chop('lfo1', 0) * 6 + 3, chop('lfo2', 0), 0.01)
  .repeat(3, 3)
  .rotate(chop('lfo3', 0))
  .invert()
  .out()
```

### Voronoi Cells
```javascript
// Cellular patterns
voronoi(chop('lfo1', 0) * 10, 0.1, chop('lfo2', 0))
  .thresh(0.5)
  .invert()
  .out()
```

### Stripes and Waves
```javascript
// Clean line work
osc(chop('lfo1', 0) * 30 + 10, 0)
  .modulate(noise(2), 0.1)
  .thresh(chop('lfo2', 0) * 0.5, 0.01)
  .invert()
  .out()
```

### Hatching Effect
```javascript
// Cross-hatching
osc(20, 0, 0).thresh(0.5)
  .add(osc(20, 0, 1.57).thresh(0.5))
  .invert()
  .out()
```

---

## Advanced Techniques

### Feedback with Decay
```javascript
osc(10, 0.1, 1.4)
  .rotate(0.01, 0.1)
  .modulate(o0, 0.9)
  .blend(o0, 0.95)
  .out()
```

### Recursive Modulation
```javascript
noise(chop('lfo1', 0) * 3)
  .modulate(
    osc(chop('lfo2', 0) * 10)
      .modulate(noise(chop('lfo3', 0) * 5))
  )
  .out()
```

### Dynamic Kaleidoscope
```javascript
shape(4)
  .kaleid(() => Math.floor(chop('lfo1', 0) * 10) + 2)
  .rotate(chop('lfo2', 0) * 3.14)
  .out()
```

### Scrolling Patterns
```javascript
osc(10, 0.1, 1)
  .scrollX(chop('lfo1', 0) * 0.1, 0)
  .scrollY(chop('lfo2', 0) * 0.1, 0)
  .out()
```

### Pixelation Effect
```javascript
src(s0)
  .pixelate(
    chop('lfo1', 0) * 100 + 10,
    chop('lfo2', 0) * 100 + 10
  )
  .out()
```

### Color Shifting
```javascript
gradient(1)
  .colorama(chop('lfo1', 0))
  .out()
```

### Blend Modes
```javascript
// Multiply blend
osc(10).mult(noise(3)).out()

// Add blend
shape(4).add(voronoi(5), 0.5).out()

// Difference blend
src(s0).diff(osc(20)).out()
```

### Time-Based Animation
```javascript
// Using time function (note: time is built into Hydra)
osc(10, 0.1, () => time * 0.1)
  .rotate(() => time * 0.05)
  .out()
```

### Conditional Effects
```javascript
// Switch between effects based on LFO value
osc(10)
  .blend(
    noise(3),
    () => chop('lfo1', 0) > 0.5 ? 1 : 0
  )
  .out()
```

### Complex Compositions
```javascript
// Layer multiple effects
gradient(1)
  .mult(osc(chop('lfo1', 0) * 20, 0.1))
  .modulate(noise(chop('lfo2', 0) * 5), 0.1)
  .color(
    chop('lfo3', 0),
    chop('lfo4', 0),
    () => a.fft[0]
  )
  .kaleid(4)
  .out()
```

---

## Tips and Tricks

### Smoothing CHOP Values
Create a Filter CHOP with low-pass filtering for smoother transitions.

### Performance Optimization
- Reduce modulation depth for faster rendering
- Use simpler patterns when targeting 60fps
- Disable unused outputs in OutputRouter

### Plotting Optimization
- Use high threshold values (0.4-0.6) for cleaner lines
- Avoid anti-aliasing (use thresh with small smoothing)
- Test edge detection thresholds: try 100/200 for best results

### Creative Workflows
1. Start with simple pattern
2. Add one modulation at a time
3. Connect to CHOPs for dynamic control
4. Save as preset when you like result
5. Iterate and experiment!

---

## Example Workflows

### Live Performance Setup
1. Load audio reactive preset
2. Connect MIDI controller to CHOPs
3. Map controls to key parameters
4. Switch between scenes for variety

### Generative Art Session
1. Load generative preset
2. Adjust LFO speeds for slow evolution
3. Capture interesting frames to SVG
4. Plot to AxiDraw for physical output

### Video Processing Pipeline
1. Initialize webcam
2. Apply feedback effect
3. Layer with generative patterns
4. Record output for video work

---

**Experiment and have fun! The possibilities are endless when combining Hydra's visual synthesis with TouchDesigner's data processing.**
