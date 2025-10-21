# Hydra Parameter Creation - Complete Guide

## Overview

Hydra Parameter Creation provides intelligent parameter synchronization between Hydra code and TouchDesigner custom parameters. It analyzes your Hydra code, automatically creates appropriately named parameters, and keeps values in sync bidirectionally.

## Features

### Intelligent Parameter Detection
- **Automatic number extraction** from Hydra code
- **Context-aware naming** based on function and position
- **Chain position tracking** (e.g., first `.rotate()` vs second `.rotate()`)
- **Instance differentiation** - Multiple `osc()` calls get unique names
- **RGB color grouping** - `.color(r, g, b)` creates unified color picker

### Smart Filtering
The system intelligently skips numbers that shouldn't be parameters:
- **Template references**: `{{null6.0}}` - Dynamic values from other systems
- **Arrow functions**: `() => Math.sin(time)` - Expressions using time/math
- **Built-in values**: `time`, `Math.PI`, `frame`, `width`, `height`
- **Special patterns**: Numbers following reserved keywords

### TouchDesigner Integration
- **TD-compliant naming**: CamelCase with proper capitalization
- **Wide value ranges**: -1000 to 1000, no clamping
- **RGB parameters**: Uses `appendRGB()` for color values
- **Persistent parameters**: Creates only missing parameters, keeps existing

### Performance Optimized
- **Pre-processing**: Code structure analyzed once
- **Binary search**: O(log n) function lookup
- **Minimal overhead**: Fast sync even with many parameters

### Source Tracing (NEW)
- **Automatic source detection**: Traces from CodeManager back to original textDATs
- **SelectDAT support**: Follows selectDAT `dat` parameters to find sources
- **Smart write location**: Prioritizes SceneCode > SceneCodeSender > other textDATs
- **Tag-based identification**: Uses `SceneCode` and `SceneCodeSender` tags to locate sources
- **Chain traversal**: Recursively follows input connections and parameter references

## Functions

### `sync_now()`
**Reads values from current Hydra code and updates parameter sliders**

**What it does:**
1. Gets the currently active scene code
2. Extracts all valid numbers from the code
3. Analyzes context to generate intelligent parameter names
4. Creates any missing parameters
5. Updates all parameter values to match the code

**Example:**
```python
sync_now()
```

**Output:**
```
=== SYNCING FROM CURRENT SCENE (FAST) ===
Using scene: /project1/hydra_system/code/CodeManager/scene2_code
Found 10 valid numbers: ['6', '0.1', '0.8', '1.04', '0', '-1.1', '0.1', '2', '20', '2.5']
  Created RGB parameter: Colorrgbone (Color RGB 1)
  Oscfrequency: 0.0 -> 6.0 [Osc Frequency]
  Oscsync: 0.0 -> 0.1 [Osc Sync]
  Oscoffset: 0.0 -> 0.8 [Osc Offset]
  Colorrgbone: (0.0, 0.0, 0.0) -> (1.04, 0.0, -1.1) [Color RGB 1]
SUCCESS: Synced 10 parameters from current scene
```

---

### `apply_now()`
**Writes parameter slider values back to current Hydra code with context-aware matching**

**What it does:**
1. Gets all parameter values from the HydraParams page (by name)
2. Analyzes code context to identify each number's parameter name
3. Matches parameters by name instead of position (order-independent)
4. Traces to find the original source textDAT
5. Writes changes to the editable source DAT

**Key Features:**
- **Context-aware matching**: Each number is analyzed to determine its function and parameter name
- **Name-based replacement**: Parameters matched by name (e.g., `Oscfrequency`) not by index
- **Order-independent**: Parameter order in UI doesn't affect code replacement
- **Smart source detection**: Automatically writes to the correct source textDAT
- **RGB expansion**: RGB parameters correctly expanded to r, g, b values

**Example:**
```python
apply_now()
```

**Output:**
```
=== APPLYING TO CURRENT SCENE ===
Reading code from: /project1/hydra_system/code/CodeManager/scene2_code
Will write changes to: /project1/scene2_code4 (original source)
Loaded 63 parameters by name

Mapping positions to parameters:
  Position 0: Oscfrequency = 48.0
  Position 1: Oscsync = -0.1
  Position 2: Oscoffset = 0.0
  Position 3: Colorrgbone.r = 0.0
  Position 4: Colorrgbone.g = 0.0
  Position 5: Colorrgbone.b = 1.0

Applying changes:
  Position 5: '1' -> '1'
  Position 4: '0' -> '0'
  Position 3: '0' -> '0'

Collected 4 DATs in chain:
  - /project1/hydra_system/code/CodeManager/scene2_code [textDAT]
  - /project1/hydra_system/code/CodeManager/select2 [selectDAT]
  - /project1/scene2_code [textDAT] (tags: SceneCodeSender)
  - /project1/scene2_code4 [textDAT] (tags: SceneCode)

Trying to write in priority order:
  Attempting: /project1/scene2_code4
  ✓ SUCCESS: Applied 63 changes to: /project1/scene2_code4
```

**Use case:** Adjust parameters with sliders, then write changes back to code. Parameters are matched intelligently regardless of their order in the parameter page.

---

### `remove_unused_parameters()`
**Removes parameters that aren't needed for the current scene**

**What it does:**
1. Analyzes current scene to determine needed parameters
2. Compares with existing parameters
3. Removes parameters whose names don't match anything in the scene
4. Keeps all parameters actually used

**Example:**
```python
remove_unused_parameters()
```

**Output:**
```
=== REMOVING UNUSED PARAMETERS ===
Analyzing scene: /project1/hydra_system/code/CodeManager/scene2_code
Current scene needs 7 parameters: ['Colorrgbone', 'Oscfrequency', 'Oscsync', ...]
Found 12 user parameters, 5 are unused
  Removed: OldParam1
  Removed: OldParam2
SUCCESS: Removed 5 unused parameters
```

**Use case:** Clean up after switching scenes or editing code

---

### `cleanup_and_sync()`
**Removes unused parameters, then syncs with current scene**

**What it does:**
1. Runs `remove_unused_parameters()`
2. Runs `sync_now()`

**Example:**
```python
cleanup_and_sync()
```

**Use case:** One-step cleanup and sync when switching between scenes

---

## Parameter Naming Convention

### Basic Pattern
```
{FunctionName}{ParameterName}{ChainSuffix}{InstanceSuffix}
```

### Source Functions (Chain Position 0)
First function in the chain - no chain suffix

**Examples:**
- `osc(6, 0.1, 0.8)` →
  - `Oscfrequency` (6)
  - `Oscsync` (0.1)
  - `Oscoffset` (0.8)

- `noise(2.5, 0.1)` →
  - `Noisescale` (2.5)
  - `Noiseoffset` (0.1)

### Chained Functions (Chain Position > 0)
Functions after `.` get position suffix: `one`, `two`, `three`, etc.

**Examples:**
- `.rotate(3.14, 0.1)` (first in chain) →
  - `Rotateangleone` (3.14)
  - `Rotatespeedone` (0.1)

- `.pixelate(20, 30)` (second in chain) →
  - `Pixelatepixelxtwo` (20)
  - `Pixelatepixelytwo` (30)

### Multiple Instances
When same parameter name appears multiple times, adds letter suffix: `a`, `b`, `c`, etc.

**Examples:**
```javascript
osc(48, -0.1, 0)  // First osc
.add(
    osc(28, 0.1, 0)  // Second osc
)
.diff(
    osc(64, -0.01, 0)  // Third osc
)
```

Results in:
- `Oscfrequency` = 48
- `Oscfrequencya` = 28
- `Oscfrequencyb` = 64

### RGB Color Parameters
Color functions get grouped into single RGB parameter

**Examples:**
- `.color(1.04, 0, -1.1)` (at chain position 1) →
  - `Colorrgbone` = RGB(1.04, 0, -1.1)

- `.color(1, 0.5)` (only 2 values) →
  - `Colorrgbone` = RGB(1, 0.5, 0) // Blue defaults to 0

- `solid(0.8, 0.2, 0.9)` (source function) →
  - `Solidrgb` = RGB(0.8, 0.2, 0.9)

---

## Supported Hydra Functions

### Source Functions
- `osc(frequency, sync, offset)`
- `noise(scale, offset)`
- `voronoi(scale, speed, blending)`
- `shape(sides, radius, smoothing)`
- `gradient(speed)`
- `solid(r, g, b, a)` - RGB grouped

### Geometry Modifiers
- `rotate(angle, speed)`
- `scale(amount, xmult, ymult)`
- `pixelate(pixelx, pixely)`
- `repeat(repeatx, repeaty, offsetx, offsety)`
- `kaleid(nsides)`

### Color Modifiers
- `color(r, g, b, a)` - RGB grouped
- `hue(hue)`
- `saturate(amount)`
- `contrast(amount)`
- `brightness(amount)`
- `invert(amount)`
- `thresh(threshold, tolerance)`
- `colorama(amount)`

### Blend Functions
- `blend(amount)`
- `add(amount)`
- `sub(amount)`
- `mult(amount)`
- `diff(amount)`

### Modulate Functions
- `modulate(amount)`
- `modulatescale(multiple, offset)`
- `modulaterotate(multiple, offset)`
- `modulatehue(amount)`
- `modulatekaleid(nsides)`
- `modulatescrollx(scrollx, speed)`
- `modulatescrolly(scrolly, speed)`
- `modulaterepeat(repeatx, repeaty, offsetx, offsety)`

---

## Real-World Example

### Hydra Code
```javascript
speed={{null6.0}}/1000000

osc(48, -0.1, 0)
    .thresh([0.3, 0.7].fast(0.75), 0)
    .color(0, 0, 1)
    .add(
        osc(28, 0.1, 0)
            .thresh([0.3, 0.7].fast(0.75), 0)
            .rotate(3.14/4)
            .color(1, 0, 0)
            .modulateScale(osc(64, -0.01, 0))
    )
    .modulateRotate(osc(54, -0.005, 0))
    .scale(2.122)
    .out()
```

### Detected Parameters

**Source osc(48, -0.1, 0):**
- `Oscfrequency` = 48
- `Oscsync` = -0.1
- `Oscoffset` = 0

**Thresh and Color (chain position 1):**
- `Threshthresholdone` = 0.3
- `Threshtoleranceone` = 0.7
- `Fastparam1one` = 0.75
- `Fastparam2one` = 0
- `Colorrgbone` = RGB(0, 0, 1)

**Nested osc(28, 0.1, 0):**
- `Oscfrequencya` = 28
- `Oscsynca` = 0.1
- `Oscoffseta` = 0

**Nested rotate and color:**
- `Rotateangleone` = 3.14
- `Rotateangletwo` = 4 (from 3.14/4)
- `Colorrgbtwo` = RGB(1, 0, 0)

**ModulateScale osc(64, -0.01, 0):**
- `Oscfrequencyb` = 64
- `Oscsyncb` = -0.01
- `Oscoffsetb` = 0

**ModulateRotate osc(54, -0.005, 0):**
- `Oscfrequencyc` = 54
- `Oscsyncc` = -0.005
- `Oscoffsetc` = 0

**Final scale:**
- `Scaleamount` = 2.122

### What Gets Skipped
- `speed={{null6.0}}/1000000` - Contains `{{null}}` template
- `[0.3, 0.7]` arrays - Not direct function parameters
- `time` references in arrow functions
- Math operations inside expressions

---

## Workflow Tips

### Initial Setup
1. Write your Hydra code
2. Run `sync_now()` to create parameters
3. Parameters appear in direct_param_controller → HydraParams page

### Iterative Development
1. Adjust sliders in TouchDesigner
2. See real-time changes in Hydra output
3. Run `apply_now()` when satisfied to save changes to code

### Switching Scenes
1. Change to different scene
2. Run `cleanup_and_sync()` to remove old params and create new ones
3. Or run manually:
   - `remove_unused_parameters()` first
   - `sync_now()` second

### Debugging
- Check console output to see what parameters were created
- Verify parameter names match your expectations
- Use `remove_unused_parameters()` to clean up mistakes

---

## SelectDAT Workflow (NEW)

### Overview
The system now supports coding outside of the CodeManager using selectDATs and tagged textDATs. This allows you to organize your code in `/project1` and use selectDATs to route it to CodeManager.

### Setup Pattern

**Step 1: Create source textDATs in `/project1`**
- Tag with `SceneCode` for original source files
- These are your editable code files

**Step 2: Create SceneCodeSender textDATs**
- Tag with `SceneCodeSender`
- Wire inputs from `SceneCode` textDATs
- These act as intermediary pass-through DATs

**Step 3: Use selectDATs in CodeManager**
- Create selectDAT in `/project1/hydra_system/code/CodeManager/`
- Set `dat` parameter to point to SceneCodeSender
- System traces through the chain automatically

**Example Chain:**
```
/project1/scene2_code4 [SceneCode tag]
    ↓ (wired input)
/project1/scene2_code [SceneCodeSender tag]
    ↓ (dat parameter)
/project1/hydra_system/code/CodeManager/select2 [selectDAT]
    ↓ (wired input)
/project1/hydra_system/code/CodeManager/scene2_code [textDAT]
```

### How Source Tracing Works

When `apply_now()` is called:
1. **Reads** from: `/project1/hydra_system/code/CodeManager/scene2_code`
2. **Traces** through inputs and selectDAT `dat` parameters
3. **Collects** all DATs in chain: CodeManager textDAT → selectDAT → SceneCodeSender → SceneCode
4. **Writes** to: `/project1/scene2_code4` (highest priority editable source)

### Write Priority Order

The system tries writing to DATs in this order:
1. **SceneCode tagged** DATs (original sources with no inputs)
2. **SceneCodeSender tagged** DATs (pass-through DATs)
3. **Other textDATs** in the chain

### Benefits

- **Organize code in /project1**: Keep your Hydra code organized outside of deep component hierarchies
- **Edit at source**: Changes written to the original editable textDAT
- **Flexible routing**: Use selectDATs to switch between multiple source files
- **Tag-based identification**: Clear labeling system using TouchDesigner tags

### Tagging Guide

**SceneCode Tag:**
- Original source files that have no inputs
- These are the files you edit directly
- Highest priority for writing

**SceneCodeSender Tag:**
- Pass-through textDATs with inputs from SceneCode DATs
- Used to route code to CodeManager
- Second priority for writing

---

## Technical Details

### Performance Characteristics
- **Preprocessing**: O(m) where m = code length
  - Splits code into lines once
  - Finds all functions and positions once
  - Calculates chain positions once

- **Per-parameter analysis**: O(log n) where n = number of functions
  - Binary search for nearest function
  - Constant time name generation

- **Overall complexity**: O(m + p log n) where p = parameters
  - Fast even with 50+ parameters

### Parameter Value Handling
- **Range**: -1000 to 1000 (no clamping)
- **Precision**: Maintains exact values from code
- **RGB handling**: Automatically expands/contracts for apply/sync

### Code Structure Analysis
- **Chain detection**: Looks for lines starting with `.`
- **Function matching**: Regex pattern `(\w+)\s*\(`
- **Context extraction**: 100 chars before, 50 chars after each number
- **Comma counting**: Determines parameter index within function

### Source Tracing Algorithm (NEW)
- **Recursive traversal**: Follows DAT input chains recursively
- **SelectDAT handling**: Checks both wired inputs and `dat` parameters
- **Tag detection**: Identifies `SceneCode` and `SceneCodeSender` tags
- **Circular reference prevention**: Tracks visited DATs to prevent infinite loops
- **Priority sorting**: Collects all DATs, then sorts by tag priority
- **Fallback logic**: Tries multiple write locations if primary fails

### Context-Aware Parameter Matching (NEW)
- **Function context analysis**: Uses `analyze_parameter_context()` to identify each number
- **Name-based mapping**: Parameters matched by generated name (e.g., `Oscfrequency`)
- **RGB group expansion**: RGB parameters expanded to individual r, g, b values during apply
- **Order independence**: Parameter UI order doesn't affect code replacement
- **Position mapping**: Each code position mapped to parameter name before replacement

---

## Common Issues & Solutions

### Issue: Parameter showing wrong value
**Cause:** Multiple instances using same name before fix was applied

**Solution:**
```python
remove_unused_parameters()
sync_now()
```

### Issue: Too many parameters created
**Cause:** Numbers that should be skipped aren't being filtered

**Solution:** Check if numbers are in arrow functions, template references, or need new skip pattern

### Issue: Parameters not updating
**Cause:** Using wrong scene or scene not active

**Solution:** Verify correct scene is active in scene_registry table

### Issue: RGB parameter showing as three sliders
**Cause:** Function not recognized as color function or parameters not consecutive

**Solution:** Verify `.color()` or `.solid()` function, check that r,g,b values are consecutive

### Issue: "The operator is not editable" error (NEW)
**Cause:** Trying to write to a DAT that has inputs or is locked

**Solution:**
- System automatically traces to editable source DAT
- Ensure your source textDAT (with `SceneCode` tag) has no inputs
- Check that the DAT isn't locked or file-synced
- Verify tag setup: SceneCode sources should have no inputs

### Issue: Apply writes to wrong DAT (NEW)
**Cause:** Source tracing not finding the correct original textDAT

**Solution:**
1. Check that your source DAT has the `SceneCode` tag
2. Verify selectDAT `dat` parameter points to correct intermediate DAT
3. Ensure intermediate DAT has `SceneCodeSender` tag
4. Check console output to see the chain traversal:
   ```python
   apply_now()  # Watch for "Collected N DATs in chain" output
   ```

### Issue: Parameters apply to wrong positions in code (NEW)
**Cause:** Old index-based matching instead of name-based matching

**Solution:**
- Update to latest version of `manual_triggers_fixed.py`
- Run the update script:
  ```python
  exec(open(r'C:/Users/cuban/HydraToTD/scripts/update_manual_triggers.py', encoding='utf-8').read())
  ```
- New version uses context-aware matching by parameter name

### Issue: Source tracing shows unexpected DATs (NEW)
**Cause:** Incorrect tagging or wiring

**Solution:**
1. Verify tag setup:
   - Original source: `SceneCode` tag, no inputs
   - Pass-through: `SceneCodeSender` tag, input from SceneCode
   - SelectDAT: `dat` parameter pointing to SceneCodeSender
2. Check console output during `apply_now()` to see full chain
3. Use test script to debug:
   ```python
   exec(open(r'C:/Users/cuban/HydraToTD/scripts/test_source_tracing.py', encoding='utf-8').read())
   ```

---

## Future Enhancements

### Potential Features
- [ ] Preset save/load for parameter sets
- [ ] Parameter grouping by function type
- [ ] Visual feedback in TD for changed values
- [ ] Undo/redo for parameter changes
- [ ] Batch operations across multiple scenes
- [ ] Custom parameter name templates
- [ ] Parameter animation recording

---

## Installation

### Quick Install
```python
exec(open(r'C:/Users/cuban/HydraToTD/scripts/install_fixed_triggers.py').read())
```

### Update Existing Installation (NEW)
If you already have the system installed, update to get the latest features:
```python
exec(open(r'C:/Users/cuban/HydraToTD/scripts/update_manual_triggers.py', encoding='utf-8').read())
```

This updates your `/project1/hydra_system/direct_param_controller/manual_triggers` DAT with:
- Source tracing functionality
- Context-aware parameter matching
- SelectDAT workflow support

### Manual Installation
1. Copy `scripts/manual_triggers_fixed.py` to your project
2. Create DAT in `/project1/hydra_system/direct_param_controller/` named `manual_triggers`
3. Paste code into DAT
4. Add callback to your trigger buttons
5. Call functions as needed

### Testing Installation
Test that source tracing works correctly:
```python
exec(open(r'C:/Users/cuban/HydraToTD/scripts/test_source_tracing.py', encoding='utf-8').read())
```

---

## File Structure
```
HydraToTD/
├── scripts/
│   ├── manual_triggers_fixed.py        # Main system (with source tracing)
│   ├── install_fixed_triggers.py       # Initial installer script
│   ├── update_manual_triggers.py       # Update existing installation (NEW)
│   ├── test_source_tracing.py          # Test/debug source tracing (NEW)
│   ├── trace_to_source_helper.py       # Standalone tracing helper (NEW)
│   ├── export_project_structure.py     # Project documentation exporter
│   └── debugging/
│       ├── fix_*.py                     # Individual fix scripts
│       ├── manual_triggers_*.py         # Earlier versions
│       └── enhanced_tool_dat_content.py # Development scripts
└── documentation/
    └── Features/
        └── HYDRA_PARAMETER_CREATION.md # This file
```

---

## Version History

### v1.4 (Current)
- **Source tracing system**: Automatically traces from CodeManager back to original textDATs
- **SelectDAT workflow**: Support for coding outside CodeManager using selectDATs
- **Context-aware parameter matching**: apply_now() now matches parameters by name, not index
- **Tag-based identification**: SceneCode and SceneCodeSender tags for source management
- **Smart write location**: Prioritizes editable sources when writing changes
- **Order-independent apply**: Parameters can be in any order in UI
- **Chain traversal**: Recursive DAT input following with circular reference prevention
- **Update script**: New update_manual_triggers.py for easy updates
- **Test utilities**: Added test_source_tracing.py for debugging

### v1.3
- Added instance tracking for duplicate parameter names
- Performance optimization with preprocessing
- Binary search for O(log n) lookups
- RGB color parameter grouping
- Name-based parameter cleanup

### v1.2
- Fixed chain position calculation
- Arrow function detection
- Template reference filtering
- Removed parameter clamping

### v1.1
- Context-aware parameter naming
- Smart number filtering
- TD-compliant naming convention

### v1.0
- Initial release
- Basic sync and apply functionality

---

## Support

For issues, questions, or feature requests, refer to:
- Main project documentation in `CLAUDE.md`
- Architecture details in `Architecture.md`
- Implementation guide in `Hydra-TouchDesigner Implementation Blueprint.md`

---

*Last updated: 2025-10-20 - v1.4 with source tracing and context-aware parameter matching*
