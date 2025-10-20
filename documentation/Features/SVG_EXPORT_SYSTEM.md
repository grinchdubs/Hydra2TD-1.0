# SVG Export and AxiDraw Plotting System

## Overview

The HydraToTD project includes a complete SVG export and AxiDraw plotting system that converts live Hydra visual synthesis output into plottable vector graphics. The system captures edge-detected frames from Hydra patterns and exports them as SVG files suitable for pen plotting with an AxiDraw machine.

## System Architecture

### 1. Edge Detection Pipeline

Located at: `/project1/hydra_system/SVGExporter`

**Pipeline Flow:**
```
select_main (Select TOP)
  ↓
edge_detect1 (Edge TOP) - Detects edges in Hydra output
  ↓
level_adjust (Level TOP) - Adjusts contrast and brightness
  ↓
null1 (Null TOP)
  ↓
normal1 (Normal Map TOP) - Normalizes edge data
  ↓
cache1 (Cache TOP) - Caches processed frame
  ↓
trace2 (Trace TOP) - Converts raster to vector
  ↓
toptoSVG component - Main SVG export system
```

**Key Parameters:**
- **Edge Detection Threshold**: Adjusted via `thresholds` CHOP
- **Level Adjust**: Controls contrast and brightness of edges
- **Cache**: Holds frame for processing without blocking real-time rendering

### 2. toptoSVG Component

Located at: `/project1/hydra_system/SVGExporter/toptoSVG`

This is a custom SOP-based SVG export system that converts TouchDesigner geometry into plottable SVG files.

**Features:**
- Converts SOPs (Surface Operators) directly to SVG paths
- Supports polylines and polygons
- Configurable canvas size (width/height in inches/mm)
- DPI selector for different target applications
- RGB stroke color control
- Stroke width adjustment
- Zoom/scaling controls

**Core Module: Soptosvg Class**

Based on Matthew Ragan's SOPtoSVG system with enhancements by Kris Northern.

```python
class Soptosvg:
    def Save(self):
        # Main export method
        # Converts SOP geometry to SVG file
        # Handles polylines, polygons, or both
```

**Key Methods:**
- `Save()` - Exports current geometry to SVG
- `SavePolyline()` - Exports unclosed line paths
- `SavePolygon()` - Exports closed polygon paths
- `WorldToCam()` - Converts world space to camera space
- `Canvas_size()` - Returns canvas dimensions
- `Par_check()` - Validates parameters before export

**Export Settings:**
- **Canvas Size**: Configurable via `Canvasmm1` (width) and `Canvasmm2` (height)
- **DPI**: Switchable between 72 DPI (Illustrator) and 96 DPI (Inkscape)
- **Stroke Color**: RGB values (0-1 range)
- **Stroke Width**: Configurable line weight
- **Zoom/Scalar**: Scales geometry to canvas

**File Output:**
- Directory: `C:/Users/cuban/HydraToTD/svg_exports/`
- Filename format: Set via parameters in toptoSVG component
- SVG format: Tiny profile with viewBox for proper scaling

### 3. Button Interface

Located at: `/project1/hydra_system/SVGExporter/export_buttons`

**Available Buttons:**
- **Capture Main** - Exports main Hydra output to SVG
- **Capture O0** - Exports output 0 to SVG
- **Capture O1** - Exports output 1 to SVG
- **Capture O2** - Exports output 2 to SVG
- **Capture O3** - Exports output 3 to SVG
- **Capture & Plot Main** - Exports and immediately sends to AxiDraw
- **Plot Recent** - Plots the most recently created SVG file
- **List Exports** - Lists all exported SVG files

**Button Callbacks:**

Located at: `/project1/hydra_system/SVGExporter/button_callbacks` (Panel Execute DAT)

The callbacks handle button presses and route to appropriate export/plot functions.

### 4. AxiDraw Plotting System

**Architecture:**

The plotting system uses an external Python process to communicate with the AxiDraw, allowing TouchDesigner to remain responsive during plotting.

**Components:**

1. **External Plotting Module** (`plot_svg_external.py`)
   - Runs in system Python (not TouchDesigner's embedded Python)
   - Uses `pyaxidraw` library for AxiDraw control
   - Runs asynchronously via `subprocess.Popen()`
   - Location: `C:/Users/cuban/HydraToTD/scripts/plot_svg_external.py`

2. **Key Functions:**

```python
def plotSVGExternal(svg_path):
    """
    Plot SVG file using external Python with pyaxidraw
    Runs in background - TouchDesigner stays responsive
    Returns immediately, plotting happens asynchronously
    """

def plotSVGExternalWait(svg_path, timeout=300):
    """
    Plot SVG and wait for completion (blocking version)
    Use when you need to ensure plot finishes before continuing
    """
```

**AxiDraw Configuration:**

Default plotting parameters (in `plot_svg_external.py`):
```python
ad.options.penlift = 3
ad.options.speed_pendown = 50      # Pen-down speed
ad.options.speed_penup = 75        # Pen-up speed
ad.options.accel = 75              # Acceleration
ad.options.pen_pos_down = 40       # Pen down position
ad.options.pen_pos_up = 60         # Pen up position
ad.options.pen_rate_lower = 50     # Pen lowering speed
ad.options.pen_rate_raise = 75     # Pen raising speed
```

**Python Environment:**

- System Python: `C:\Users\cuban\AppData\Local\Programs\Python\Python310\python.exe`
- Required Package: `pyaxidraw` (AxiDraw API)
- Installation: `pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip`

### 5. Integration with TouchDesigner

**Async Plotting Flow:**

```
User clicks "Capture & Plot Main"
  ↓
Button callback triggers SVG export via toptoSVG.Save()
  ↓
SVG file written to disk
  ↓
Button callback imports plot_svg_external module
  ↓
plotSVGExternal() spawns external Python process
  ↓
External process loads SVG and sends to AxiDraw
  ↓
TouchDesigner continues running (non-blocking)
```

**Why External Python?**

TouchDesigner uses an embedded Python 3.11 environment that doesn't include `pyaxidraw`. Rather than trying to install it in TouchDesigner's Python, we use the system Python where `pyaxidraw` is already installed. This approach:
- Avoids TouchDesigner crashes from incompatible packages
- Keeps plotting async (TD doesn't freeze during plot)
- Allows independent AxiDraw control outside TouchDesigner

## Usage

### Exporting an SVG

1. **Live Capture:**
   - Run Hydra patterns in Web Render TOP
   - Edge detection pipeline processes output automatically
   - Click "Capture Main" (or O0-O3 for specific outputs)
   - SVG saved to `svg_exports/` directory

2. **Manual Export:**
   - Navigate to `/project1/hydra_system/SVGExporter/toptoSVG`
   - Click the "SAVE" button
   - Configure parameters:
     - Canvas size (width/height)
     - DPI setting
     - Stroke color/width
     - Output filename

### Plotting an SVG

1. **Immediate Plot:**
   - Click "Capture & Plot Main"
   - Captures current frame and sends to AxiDraw
   - TouchDesigner remains responsive during plot

2. **Plot Previous Export:**
   - Click "Plot Recent"
   - Plots most recently created SVG file
   - Useful for re-plotting without recapturing

3. **Direct Plot (External):**
   ```python
   # From command line or external script
   python C:/Users/cuban/HydraToTD/scripts/plot_svg_external.py <svg_path>
   ```

### Listing Exports

Click "List Exports" to see the 10 most recent SVG files:
```
Found 14 SVG exports:
  hydra_numpy_main_20251012_031924.svg
  hydra_numpy_main_20251012_031810.svg
  ...
```

## File Structure

```
C:/Users/cuban/HydraToTD/
├── svg_exports/                    # All exported SVG files
├── scripts/
│   ├── plot_svg_external.py        # External AxiDraw plotting
│   ├── update_numpy_export_external_plot.py
│   ├── create_numpy_svg_export.py  # Legacy numpy approach
│   ├── create_pillow_svg_export.py # Legacy PIL approach
│   ├── create_sop_svg_pipeline.py  # Legacy SOP approach
│   └── test_plot_recent.py         # Diagnostic script
└── TouchDesigner Project
    └── /project1/hydra_system/SVGExporter/
        ├── select_main             # Input selection
        ├── edge_detect1            # Edge detection
        ├── level_adjust            # Contrast/brightness
        ├── cache1                  # Frame caching
        ├── trace2                  # Vector tracing
        ├── toptoSVG/               # Main export system
        │   ├── SOPtoSVG/           # Geometry processing
        │   └── SAVE button         # Export trigger
        ├── export_buttons/         # UI buttons
        │   ├── capture_main
        │   ├── capture_o0-o3
        │   ├── plot_main
        │   ├── plot_recent
        │   └── list_exports
        └── button_callbacks        # Panel Execute DAT
```

## Technical Notes

### DPI and Application Compatibility

From the Soptosvg class documentation:

> Inkscape and Illustrator interpret values differently. Both programs use 11x17" canvas at 431.8mm x 279.4mm, but:
> - **Illustrator**: 72 DPI (1224x792 pixels)
> - **Inkscape**: 96 DPI (1632x1056 pixels)

The system includes a DPI selector to ensure proper scaling in your target application.

### Coordinate Space Conversion

TouchDesigner SOPs use -1 to +1 coordinate space by default. The export system:
1. Scales geometry by the shortest canvas dimension
2. Calculates offset to center geometry
3. Converts Y-axis (TD uses +Y up, SVG uses +Y down)

Formula from code:
```python
Scalar = float(parent.svg.par.Canvasmm2) * Zoom
newX = (vert.point.x * Scalar) + xOffset
newY = (-vert.point.y * Scalar) + yOffset  # Note Y-axis flip
```

### Edge Detection Tuning

Key parameters for quality SVG output:

1. **Edge TOP Threshold**: Controls what is detected as an edge
2. **Level TOP**:
   - `inhigh`: Upper brightness threshold
   - `gamma1`: Gamma correction
   - `brightness1`: Overall brightness boost
3. **Trace TOP**: Converts raster edges to vector paths

### Performance Considerations

- **Async Plotting**: Using external Python process prevents TouchDesigner from freezing
- **Cache TOP**: Buffers frame so edge detection doesn't block rendering
- **Sample Rate**: Downsampling can improve performance for large images
- **Path Simplification**: Reducing vertex count improves plot speed

## Troubleshooting

### "pyaxidraw not installed" Error

**Cause**: TouchDesigner's embedded Python doesn't have pyaxidraw

**Solution**: The system now uses external Python automatically. Ensure:
1. System Python is installed at: `C:\Users\cuban\AppData\Local\Programs\Python\Python310\python.exe`
2. pyaxidraw is installed in system Python:
   ```bash
   pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip
   ```

### TouchDesigner Freezes During Plot

**Cause**: Using blocking plot method instead of async

**Solution**: Ensure `plotSVGExternal()` is used (not `plotSVGExternalWait()`)

### Empty SVG Files

**Cause**: Edge detection threshold too high or no geometry generated

**Solution**:
1. Check edge detection parameters
2. Verify geometry exists in SOP chain
3. Check `thresholds` CHOP values

### Plot Recent Button Not Working

**Cause**: Module not reloaded or path incorrect

**Solution**: Run diagnostic script:
```python
exec(open('C:/Users/cuban/HydraToTD/scripts/test_plot_recent.py').read())
```

## Future Enhancements

Potential improvements to the system:

1. **Multi-output SVG Export**: Currently focuses on main output, could expand to all 4 outputs
2. **Layer Support**: Export different Hydra buffers to separate SVG layers
3. **Color Support**: Multi-pen AxiDraw plotting with color information
4. **Path Optimization**: Reduce pen travel time with path sorting algorithms
5. **Live Preview**: Show SVG preview before plotting
6. **Batch Export**: Capture sequence of frames for animation plotting
7. **Plot Queue**: Queue multiple SVGs for sequential plotting

## References

- **AxiDraw Documentation**: http://wiki.evilmadscientist.com/AxiDraw
- **AxiDraw PDF Manual**: http://cdn.evilmadscientist.com/wiki/axidraw/software/AxiDraw_V33.pdf
- **svgwrite Library**: http://svgwrite.readthedocs.io/en/latest/svgwrite.html
- **TouchDesigner**: https://derivative.ca
- **Hydra**: https://hydra.ojack.xyz

## Credits

- **toptoSVG System**: Based on Matthew Ragan's SOPtoSVG
- **Enhancements**: Kris Northern (@krisnorthern)
- **AxiDraw Integration**: Custom implementation for HydraToTD project
- **Async Plotting**: External Python process approach

---

*Last Updated: 2025-10-12*
